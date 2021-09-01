import random
from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator

class RandomShift(SolutionMethod):

    def __init__(self, name):
        super().__init__(name)

    def initialize_class_attributes(self):
        return super().initialize_class_attributes()


    def solve(self, solution, parameters):
        new_solution = solution.copy()

        request_to_move = random.choice(new_solution.requests())

        route_pos = new_solution.get_request_route(request_to_move)

        RemovalOperator().try_to_remove(
            new_solution.routes[route_pos],
            request_to_move,
            self.obj_func,
            self.constraints
        )


    def update_route_values(self, route, position, request):
        pass
    

    def get_attr_relation_reader_heuristic(self):
        return {}