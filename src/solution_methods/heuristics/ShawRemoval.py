from abc import ABCMeta, abstractclassmethod, abstractmethod

import random
from src.exceptions import CouldNotRemoveWithShawRemoval

import numpy

from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.heuristics.RemovalHeuristic import RemovalHeuristic

class ShawRemoval(RemovalHeuristic, metaclass=ABCMeta):


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.p = None


    def solve(self, solution, parameters):
        number_of_removals = parameters["b"]
        randomization_parameter = self.p

        request = random.choice(list(solution.requests()))
        requests_to_remove = {request}
        while (len(requests_to_remove) < number_of_removals):
            request = random.choice(list(solution.requests()))
            candidates = solution.requests() - requests_to_remove
            related_measure = self.calculate_requests_relatedness_measure(
                solution, 
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
        
        for route_pos in range(solution.number_of_routes()):
            for request in requests_to_remove:
                self.remove_from_route(route_pos, request, solution)

        return solution


    def remove_from_route(self, route_pos, request, solution):
        route = solution.routes[route_pos]
        if (request in route):
            new_route = self.try_to_remove(
                solution.routes[route_pos], 
                request
            )
            if (new_route is None):
                raise CouldNotRemoveWithShawRemoval(request)
            else:
                request_pos = route.index(request)
                solution.remove_request(request)
                solution.set_route(route_pos, new_route)
                self.update_solution_requests_costs_after_removal(
                    solution, 
                    new_route,
                    request_pos,
                    request
                )


    def get_request_to_remove(self, candidates, values, position):
        list_candidates = [key for key in candidates]
        list_candidates_values = [values[i] for i in list_candidates]
        request_position = numpy.argpartition(
            numpy.array(list_candidates_values) * -1,
            position
        )

        return list_candidates[request_position[position]]



    @abstractclassmethod
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

    def try_to_remove(self, route, request):
        return super().try_to_remove(route, request)

