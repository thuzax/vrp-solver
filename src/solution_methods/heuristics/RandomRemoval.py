import random
from abc import ABCMeta, abstractmethod


from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator

class RandomRemoval(SolutionMethod):

    def __init__(self):
        super().__init__("Random Removal")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()

    def solve(self, solution, parameters):
        new_solution = solution.copy()
        
        routes = new_solution.routes
        number_of_removals = parameters["b"]

        empty_routes = []
        for i in range(number_of_removals):
            route_pos = random.randint(0, len(routes)-1)
            
            if (routes[route_pos].empty()):
                i -= 1
                empty_routes.append(routes[route_pos])
                routes.pop(route_pos)
                continue
            
            request = random.choice(list(routes[route_pos].requests()))
            request_pos = routes[route_pos].index(request)

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
        
        routes += empty_routes
        return new_solution

    def get_attr_relation_reader_heuristic(self):
        return {}

    def update_route_values(self, route, position, request):
        return super().update_route_values(route, position, request)