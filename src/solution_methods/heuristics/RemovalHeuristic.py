from abc import ABCMeta, abstractmethod

from src.solution_methods.SolutionMethod import SolutionMethod

class RemovalHeuristic(SolutionMethod, metaclass=ABCMeta):

    def __init__(self, name):
        super().__init__(name)


    @abstractmethod
    def try_to_remove(self, route, request):
        copy_route = route.copy()

        position = copy_route.index(request)
        copy_route.pop(position)


        self.update_route_values(copy_route, position, request)

        copy_route.route_cost = (
            self.obj_func.route_reduced_cost_after_insertion(
                route,
                position, 
                request
            )
        )

        if (self.route_is_feasible(copy_route)):
            return copy_route


    