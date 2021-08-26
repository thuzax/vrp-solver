from abc import ABCMeta, abstractmethod

from numpy import copy
from src.solution_methods.SolutionMethod import SolutionMethod

class InsertionHeuristic(SolutionMethod, metaclass=ABCMeta):

    def __init__(self, name):
        super().__init__(name)


    @abstractmethod
    def try_to_insert(self, route, position, request, obj_func):
        copy_route = route.copy()
        copy_route.insert(position, request)

        self.update_route_values(copy_route, position, request, obj_func)

        if (self.route_is_feasible(copy_route)):
            return copy_route


    