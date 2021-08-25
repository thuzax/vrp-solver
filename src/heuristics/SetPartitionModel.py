
from src.heuristics.Heuristic import Heuristic

from src.heuristics.Heuristic import Heuristic

class SetPartitionModel(Heuristic):
    
    def __init__(self):
        if (not hasattr(self, "name")):
            super().__init__("SetPartitionModel")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def solve(self, parameters):
        super().solve()


    def update_route_values(self, route, position, request, obj_func):
        super().update_route_values(route, position, request, obj_func)


    @staticmethod
    def get_attr_relation_reader_heuristic():
        rela_reader_heur = Heuristic.get_attr_relation_reader_heuristic()
        return rela_reader_heur