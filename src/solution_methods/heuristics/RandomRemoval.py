from abc import ABCMeta, abstractmethod

import random

from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.heuristics.RemovalHeuristic import RemovalHeuristic

class RandomRemoval(RemovalHeuristic, metaclass=ABCMeta):


    def initialize_class_attributes(self):
        self.execution_probability = None


    def solve(self, parameters):
        requests = parameters["requests"]
        routes = parameters["routes"]
        number_of_removals = parameters["b"]
        empty_routes = []
        for i in range(number_of_removals):
            route_pos = random.randint(0, len(routes)-1)
            
            if (routes[route_pos].empty()):
                i -= 1
                empty_routes.append(routes[route_pos])
                routes.pop(route_pos)
                continue
            
            request = random.choice(list(routes[route_pos].get_requests_set()))

            new_route = self.try_to_remove(routes[route_pos], request)
            if (new_route is not None):
                routes[route_pos] = new_route
                requests.remove(request)


        routes += empty_routes


    def try_to_remove(self, route, request):
        return super().try_to_remove(route, request)

    