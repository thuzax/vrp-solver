
from src.heuristics.Heuristic import Heuristic

from src.heuristics.Heuristic import Heuristic

class AGES(Heuristic):

    def __init__(self):
        super().__init__("AGES")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def solve(self, parameters):
        super().solve()


    @staticmethod
    def get_attr_relation_reader_heuristic():
        rela_reader_heur = Heuristic.get_attr_relation_reader_heuristic()
        return rela_reader_heur