
from src.heuristics.Heuristic import Heuristic

from src.heuristics.Heuristic import Heuristic

class SetPartitionModel(Heuristic):
    
    def __init__(self):
        super().__init__("SetPartitionModel")

    def solve(self, parameters):
        super().solve()

    @staticmethod
    def get_attr_relation_reader_heuristic():
        rela_reader_heur = Heuristic.get_attr_relation_reader_heuristic()
        return rela_reader_heur