from abc import ABCMeta, abstractmethod

import random

from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.heuristics.RemovalHeuristic import RemovalHeuristic

class WorstRemoval(RemovalHeuristic, metaclass=ABCMeta):


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.p = None


    def solve(self, solution, parameters):
        routes = solution.routes
        number_of_removals = parameters["b"]
        randomization_parameter = self.p
        
        for i in range(number_of_removals):
            requests_costs = solution.requests_costs()
            sorted_requests_tuple = sorted(
                requests_costs.items(), 
                key=lambda x: x[1], 
                reverse=True
            )

            sorted_requests = [x for x, y in sorted_requests_tuple]
            random_multiplier = random.uniform(0, 0.9999999999)
            # random_multiplier = random.randint(0, 999)/1000.0
            request_sort_position = int(
                (random_multiplier**randomization_parameter) 
                * len(sorted_requests)
            )
            request = sorted_requests[request_sort_position]
            route = solution.get_request_route(request)
            request_pos = route.index(request)

            route_pos = routes.index(route)
            
            new_route = self.try_to_remove(routes[route_pos], request)
            if (new_route is not None):
                solution.remove_request(request)
                solution.set_route(route_pos, new_route)
                self.update_solution_requests_costs_after_removal(
                    solution, 
                    new_route,
                    request_pos,
                    request
                )

        return solution

    def try_to_remove(self, route, request):
        return super().try_to_remove(route, request)
