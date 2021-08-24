from abc import ABCMeta, abstractmethod

from numpy import copy
from src.heuristics.Heuristic import Heuristic

class InsertionHeuristic(Heuristic, metaclass=ABCMeta):

    def __init__(self, name):
        if (not hasattr(self, "name")):
            super().__init__(name)

    @abstractmethod
    def try_to_insert(self, route, positions, request, obj_func):
        copy_route = route.copy()
        copy_route.insert(positions, request, obj_func)

        if (self.route_is_feasible(copy_route)):
            return copy_route
