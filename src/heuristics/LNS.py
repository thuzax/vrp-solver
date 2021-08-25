
from src.heuristics.Heuristic import Heuristic

from src.heuristics.Heuristic import Heuristic

class LNS(Heuristic):
    

    def __init__(self):
        super().__init__("LNS")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def solve(self, parameters):
        if (not hasattr(self, "name")):
            super().solve()


    def update_route_values(self, route, position, request, obj_func):
        super().update_route_values(route, position, request, obj_func)


    @staticmethod
    def get_attr_relation_reader_heuristic():
        rela_reader_heur = Heuristic.get_attr_relation_reader_heuristic()
        return rela_reader_heur