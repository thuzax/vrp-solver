from abc import ABCMeta, abstractmethod

import random
from src.constraints.FixedRequests import FixedRequests
from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator
from src import file_log

from src.solution_methods.SolutionMethod import SolutionMethod


class WorstRemoval(SolutionMethod):


    def __init__(self):
        super().__init__("Worst Removal Ropke and Psinger 2006")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.p = None


    def solve(self, solution, parameters):
        new_solution = solution.copy()
        routes = new_solution.routes()
        number_of_removals = parameters["b"]
        randomization_parameter = self.p
        
        for i in range(number_of_removals):
            requests_costs = new_solution.requests_costs()
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
            if (request_sort_position >= len(sorted_requests)):
                request_sort_position -= 1
            
            if (len(sorted_requests) == 0):
                return new_solution

            request = sorted_requests[request_sort_position]
            route_pos, route = new_solution.get_request_route(request)
            request_pos = route.index(request)
            
            new_route = RemovalOperator().try_to_remove(
                routes[route_pos],
                request,
                self.obj_func,
                self.constraints
            )
            if (new_route is not None):
                new_solution = RemovalOperator().remove_request_from_solution(
                    new_solution,
                    request,
                    request_pos,
                    new_route,
                    route_pos,
                    self.obj_func
                )
                
        return new_solution


    def get_current_best_solution(self):
        return super().get_current_best_solution()

    def get_attr_relation_reader(self):
        return {}

