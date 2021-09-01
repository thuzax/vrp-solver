
from src.solution_methods.SolutionMethod import SolutionMethod

from src.solution_methods.SolutionMethod import SolutionMethod

class SetPartitionModel(SolutionMethod):
    
    def __init__(self):
        if (not hasattr(self, "name")):
            super().__init__("SetPartitionModel")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def solve(self, solution, parameters):
        super().solve()


    def update_route_values(self, route, position, request):
        super().update_route_values(route, position, request)


    def get_attr_relation_reader_heuristic(self):
        rela_reader_heur = super().get_attr_relation_reader_heuristic()
        return rela_reader_heur