from src import heuristics
from src.ObjectsManager import ObjectsManager

class HeuristicsObjects(ObjectsManager):
    def add_object(self, obj):
        self.add_object_of_class(obj, heuristics.Heuristic)

