import random
from src.solution_methods.SolutionMethod import SolutionMethod

class RandomShift(SolutionMethod):

    def __init__(self, name):
        super().__init__(name)

    def initialize_class_attributes(self):
        return super().initialize_class_attributes()


    def solve(self, solution, parameters):
        new_solution = solution.copy()

        request_to_move = random.choice(new_solution.requests())



    def update_route_values(self, route, position, request):
        pass
    

    def get_attr_relation_reader_heuristic(self):
        return {}