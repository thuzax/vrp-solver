
from src.solution_methods.SolutionMethod import SolutionMethod

from src.solution_methods.SolutionMethod import SolutionMethod

class AGES(SolutionMethod):

    def __init__(self):
        super().__init__("AGES")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def solve(self, parameters):
        super().solve()


    def update_route_values(self, route, position, request, obj_func):
        super().update_route_values(route, position, request, obj_func)


    @staticmethod
    def get_attr_relation_reader_heuristic():
        rela_reader_heur = SolutionMethod.get_attr_relation_reader_heuristic()
        return rela_reader_heur