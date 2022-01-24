from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
import numpy
import bisect
import math

from src.objective_functions import *
from src.route_classes.Route import *


class WKRegret(SolutionMethod):

    def __init__(self):
        super().__init__("WKRegret")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.non_insertion_cost = None


    def get_indices_best_routes(self, routes, k):
        if (len(routes) == 1):
            return [0]

        costs_arr = numpy.array([route.cost() for route in routes])
        partition = numpy.argpartition(costs_arr, k)
        best_routes = partition[:k].tolist()

        return best_routes


    def get_number_of_indices_best_routes(self):
        pass


    def solve(self, solution, parameters):
        new_solution = solution.copy()
        routes = new_solution.routes
        requests = parameters["requests_set"]
        self.k = parameters["k"]
        
        inserted = True
        i = 0
        while (inserted and len(requests) > 0):
            best_routes_ids = self.get_indices_best_routes(routes, self.k)
            # best_routes_ids = [i for i in range(len(routes))]
            regret_sets = self.get_regret_data(
                requests, 
                routes, 
                best_routes_ids
            )
            can_be_inserted = regret_sets["can_be_inserted"]
            regret_values = regret_sets["regret_values"]
            regret_routes = regret_sets["regret_routes"]
            regret_routes_ids = regret_sets["regret_routes_ids"]
            regret_insert_pos = regret_sets["regret_insert_pos"]
            
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


            route_pos = regret_routes_ids[request][0]
            inserted_position = regret_insert_pos[request][0]

            new_route = regret_routes[request][0]
            new_solution = InsertionOperator().insert_request_in_solution(
                new_solution,
                request,
                inserted_position,
                new_route,
                route_pos,
                self.obj_func
            )

            requests.remove(request)
        return new_solution


    def get_best_insertions_in_routes(self, request, routes, best_routes_pos):
        request_k_routes = []
        request_k_insertions = []
        request_k_costs = []
        routes_pos = []

        for i in best_routes_pos:
            route = routes[i]
            position, new_route, insert_cost = (
                InsertionOperator().get_best_insertion_in_route(
                    route, 
                    request,
                    self.obj_func,
                    self.constraints
                )
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
            routes_pos.insert(order_position, i)

        return (
            routes_pos,
            request_k_routes,
            request_k_insertions,
            request_k_costs
        )


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
        regret_insert_pos = {}

        for request in requests:
            routes_pos, request_routes, request_insert_pos, routes_costs = (
                self.get_best_insertions_in_routes(
                    request, 
                    routes, 
                    best_routes_ids
                )
            )

            regret_value = self.get_regret_value(routes_costs)
            
            regret_values[request] = regret_value
            regret_routes[request] = request_routes
            regret_routes_ids[request] = routes_pos
            regret_insert_pos[request] = request_insert_pos

        requests_can_be_inserted = {}
        for request in requests:
            requests_can_be_inserted[request] = (
                self.verify_if_request_has_regret_route(regret_routes[request])
            )

        
        return {
            "can_be_inserted" : requests_can_be_inserted,
            "regret_values" : regret_values,
            "regret_routes" : regret_routes,
            "regret_routes_ids" : regret_routes_ids,
            "regret_insert_pos" : regret_insert_pos
        }


    def verify_if_request_has_regret_route(self, routes):
        can_be_inserted = False
        i = 0
        while ((i < len(routes)) and (not can_be_inserted)):
            route = routes[i]
            if (route is not None):
                can_be_inserted = True
            i += 1
            continue
            
        return can_be_inserted


    def get_current_best_solution(self):
        return super().get_current_best_solution()

    def update_route_values(self, route, position, request):
        pass
    

    def get_attr_relation_reader_heuristic(self):
        return {}

