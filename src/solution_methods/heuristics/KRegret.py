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


    def solve(self, solution, parameters):
        routes = solution.routes
        requests = parameters["requests"]
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



            route_id = regret_routes_ids[request][0]
            inserted_position = regret_insert_pos[request][0]

            new_route = regret_routes[request][0]
            
            solution.set_route(route_id, new_route)
            solution.add_request(request)

            self.update_solution_requests_costs_after_insertion(
                solution, 
                new_route, 
                inserted_position,
                request
            )


            requests.remove(request)

        return solution



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
            route_ids, request_routes, request_insert_pos, routes_costs = (
                self.get_best_insertions_in_routes(
                    request, 
                    routes, 
                    best_routes_ids
                )
            )
            
            regret_value = self.get_regret_value(routes_costs)
            
            regret_values[request] = regret_value
            regret_routes[request] = request_routes
            regret_routes_ids[request] = route_ids
            regret_insert_pos[request] = request_insert_pos

        requests_can_be_inserted = {}
        for request in requests:
            requests_can_be_inserted[request] = (
                self.verify_if_insertion_is_possible(regret_routes[request])
            )
        
        return {
            "can_be_inserted" : requests_can_be_inserted,
            "regret_values" : regret_values,
            "regret_routes" : regret_routes,
            "regret_routes_ids" : regret_routes_ids,
            "regret_insert_pos" : regret_insert_pos
        }
