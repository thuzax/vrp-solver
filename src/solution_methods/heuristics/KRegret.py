import numpy
import bisect
import math

from src.objective_functions import *
from src.route_classes.Route import *
from src.solution_methods.heuristics import InsertionHeuristic


class KRegret(InsertionHeuristic, metaclass=ABCMeta):
    

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.non_insertion_cost = None


    def try_to_insert(self, route, positions, request):
        return super().try_to_insert(route, positions, request)


    def get_indices_best_routes(self, routes, k):
        if (len(routes) == 1):
            return [0]

        costs_arr = numpy.array([route.cost() for route in routes])
        partition = numpy.argpartition(costs_arr, k)
        best_routes = partition[:k].tolist()

        return best_routes


    def solve(self, parameters):
        requests = parameters["requests"]
        routes = parameters["routes"]
        k = parameters["k"]

        inserted = True
        while (inserted and len(requests) > 0):
            best_routes_ids = self.get_indices_best_routes(routes, k)
            regret_sets = self.get_regret_data(
                requests, 
                routes, 
                best_routes_ids
            )
            
            can_be_inserted = regret_sets["can_be_inserted"]
            regret_values = regret_sets["regret_values"]
            regret_routes = regret_sets["regret_routes"]
            regret_routes_ids = regret_sets["regret_routes_ids"]

            impossibles_requests = set([
                request
                for request, possible in can_be_inserted.items()
                if (not possible)
            ])

            if (len(impossibles_requests) == len(requests)):
                inserted = False
                continue

            for request in impossibles_requests:
                regret_values.pop(request)
                regret_routes.pop(request)
                regret_routes_ids.pop(request)

            request = max(regret_values, key=regret_values.get)


            route_id = regret_routes_ids[request][0]
            routes[route_id] = regret_routes[request][0]
            requests.remove(request)


    def get_best_insertion_in_route(self, route, request):
        if (route.empty()):
            new_route = self.try_to_insert(
                route,
                (0, 1), 
                request, 
            )

            if (new_route is None):
                return (
                    None,
                    None
                )
            
            return (
                (0, 1),
                new_route
            )

        best_route = None
        best_insertion_position = None

        for i in range(route.size()+1):
            for j in range(i+1, route.size()+2):
                new_route = self.try_to_insert(
                    route, 
                    (i, j), 
                    request, 
                )
                
                if (new_route is None):
                    continue

                if (self.obj_func.route_is_better(new_route, best_route)):
                    best_route = new_route
                    best_insertion_position = (i, j)

        return (
            best_insertion_position,
            best_route
        )


    def get_best_insertions_routes(self, request, routes, best_routes_ids):
        request_k_routes = []
        request_k_insertions = []
        request_k_costs = []
        route_ids = []

        for i in best_routes_ids:
            route = routes[i]
            position, new_route = (
                self.get_best_insertion_in_route(route, request)
            )
            if (new_route is None):
                cost = self.non_insertion_cost
                new_route = None
            else:
                cost = new_route.cost()
            
            order_position = bisect.bisect(
                request_k_costs, 
                cost
            )
        
            request_k_costs.insert(order_position, cost)
            request_k_insertions.insert(order_position, position)
            request_k_routes.insert(order_position, new_route)
            route_ids.insert(order_position, i)

        return (
            route_ids,
            request_k_routes,
            request_k_costs
        )


    def verify_if_insertion_is_possible(self, routes):
        can_be_inserted = False
        i = 0
        while ((i < len(routes)) and (not can_be_inserted)):
            route = routes[i]
            if (route is not None):
                can_be_inserted = True
            i += 1
            continue
            
        return can_be_inserted


    def get_regret_value(self, routes_costs):
        regret_value = 0
        cost_best = routes_costs[0]
        for i in range(1, len(routes_costs)):
            cost_current = routes_costs[i]
            regret_value +=  cost_current - cost_best
        
        return regret_value


    def get_regret_data(self, requests, routes, best_routes_ids):
        regret_values = {}
        regret_routes = {}
        regret_routes_ids = {}

        for request in requests:
            route_ids, request_routes, routes_costs = (
                self.get_best_insertions_routes(
                    request, 
                    routes, 
                    best_routes_ids
                )
            )
            
            regret_value = self.get_regret_value(routes_costs)
            
            regret_values[request] = regret_value
            regret_routes[request] = request_routes
            regret_routes_ids[request] = route_ids

        requests_can_be_inserted = {}
        for request in requests:
            requests_can_be_inserted[request] = (
                self.verify_if_insertion_is_possible(regret_routes[request])
            )
        
        return {
            "can_be_inserted" : requests_can_be_inserted,
            "regret_values" : regret_values,
            "regret_routes" : regret_routes,
            "regret_routes_ids" : regret_routes_ids
        }
