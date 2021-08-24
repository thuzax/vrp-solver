from abc import ABCMeta, abstractmethod
from src.constraints.ConstraintObjects import ConstraintsObjects
from src.heuristics.Heuristic import Heuristic

class InsertionHeuristic(Heuristic, metaclass=ABCMeta):

    def __init__(self, name):
        super().__init__(name)

    @abstractmethod
    def try_to_insert(self, route, positions, request, obj_func):
        copy_route = route.copy()
        copy_route.insert(positions, request, obj_func)

        constraints = ConstraintsObjects().get_list()
        for constraint in self.constraints:
            constraint_respected = constraint.route_is_feasible(
                copy_route, 
                positions[0], 
                copy_route.size()-1
            )

            if (not constraint_respected):
                return None

        return copy_route
