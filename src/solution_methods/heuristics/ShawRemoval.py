from abc import ABCMeta, abstractclassmethod, abstractmethod

import random
from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator
from src.exceptions import CouldNotRemoveWithShawRemoval

import numpy

from src.solution_methods.SolutionMethod import SolutionMethod

class ShawRemoval(SolutionMethod, metaclass=ABCMeta):


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.p = None


    def solve(self, solution, parameters):
        new_solution = solution.copy()
        number_of_removals = parameters["b"]
        randomization_parameter = self.p

        request = self.choose_one_random_request_to_remove(
            new_solution.requests()
        )
        requests_to_remove = {request}
        while (len(requests_to_remove) < number_of_removals):
            request = self.choose_one_random_request_to_remove(
                new_solution.requests()
            )

            candidates = (
                new_solution.requests() 
                - requests_to_remove
                - set(self.get_exception_requests())
            )
            related_measure = self.calculate_requests_relatedness_measure(
                new_solution, 
                candidates, 
                request
            )

            random_multiplier = random.uniform(0, 0.9999999999)
            position = int(
                (random_multiplier**randomization_parameter) 
                * len(candidates)
            )

            request_to_remove = self.get_request_to_remove(
                candidates, 
                related_measure, 
                position
            )


            requests_to_remove.add(request_to_remove)
        
        for route_pos in range(new_solution.number_of_routes()):
            for request in requests_to_remove:
                self.remove_from_route(route_pos, request, new_solution)
        return new_solution


    def remove_from_route(self, route_pos, request, solution):
        route = solution.routes[route_pos]
        if (request in route):
            new_route = RemovalOperator().try_to_remove(
                solution.routes[route_pos], 
                request,
                self.obj_func,
                self.constraints
            )

            if (new_route is None):
                raise CouldNotRemoveWithShawRemoval(request)
            else:
                request_pos = route.index(request)
                solution = RemovalOperator().remove_request_from_solution(
                    solution,
                    request,
                    request_pos,
                    new_route,
                    route_pos,
                    self.obj_func
                )


    def choose_one_random_request_to_remove(self, requests):
        request = random.choice(list(requests()))
        return request


    def get_request_to_remove(self, candidates, values, position):
        list_candidates = [key for key in candidates]

        if (len(list_candidates) >= position):
            return max(list_candidates)
        
        list_candidates_values = [values[i] for i in list_candidates]
        
        request_position = numpy.argpartition(
            numpy.array(list_candidates_values) * -1,
            position
        )
        
        return list_candidates[request_position[position]]


    @abstractmethod
    def get_exception_requests(self):
        return []


    @abstractmethod
    def calculate_request_relatedness_measure(self, solution, r_1, r_2):
        pass



    def calculate_requests_relatedness_measure(
        self, 
        solution, 
        removal_candidates, 
        request
    ):
        relatedness_measure = {}
        for candidate in removal_candidates:
            relation = self.calculate_request_relatedness_measure(
                solution,
                request,
                candidate 
            )
            relatedness_measure[candidate] = relation
        return relatedness_measure


    def get_current_best_solution(self):
        return super().get_current_best_solution()