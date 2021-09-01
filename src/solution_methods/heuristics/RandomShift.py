import random

from numpy.lib.function_base import insert
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator

class RandomShift(SolutionMethod):

    def __init__(self):
        super().__init__("Random Shift")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()

    def solve(self, solution, parameters):
        new_solution = solution.copy()

        request_to_move = random.choice(list(new_solution.requests()))

        old_route = new_solution.get_request_route(request_to_move)
        
        remov_request_pos_in_route = old_route.index(request_to_move)
        
        route_pos = new_solution.find_route_position_by_id(old_route.get_id())

        new_route = RemovalOperator().try_to_remove(
            new_solution.routes[route_pos],
            request_to_move,
            self.obj_func,
            self.constraints
        )

        if (new_route is None):
            return solution

        new_solution = RemovalOperator().remove_request_from_solution(
            new_solution,
            request_to_move,
            remov_request_pos_in_route,
            new_route,
            route_pos,
            self.obj_func
        )

        feasible_positions_and_routes = (
            InsertionOperator().get_all_feasible_insertions_from_routes(
                request_to_move,
                new_solution.routes,
                self.obj_func,
                self.constraints
            )
        )

        insertion_positions = []
        routes_after_insertion = []
        for route_feasible_insertions in feasible_positions_and_routes:
            if (len(route_feasible_insertions) > 0):
                positions, routes = tuple(zip(*route_feasible_insertions))
                insertion_positions += list(positions)
                routes_after_insertion += list(routes)
        
        k = 0
        found_old_route = False
        while (k < len(routes_after_insertion) and not found_old_route):
            route_after_insertion = routes_after_insertion[k]
            if (route_after_insertion.get_id() == old_route.get_id()):
                if (insertion_positions[k] == remov_request_pos_in_route):
                    found_old_route = True
                    continue
            k += 1


        route_inserted_pos = random.randint(0, len(routes_after_insertion)-1)
        route_inserted = routes_after_insertion[route_inserted_pos]
        
        route_pos_in_sol = new_solution.find_route_position_by_id(
            route_inserted.get_id()
        )

        position_insertion = insertion_positions[route_inserted_pos]

        InsertionOperator().insert_request_in_solution(
            new_solution,
            request_to_move,
            position_insertion,
            route_inserted,
            route_pos_in_sol,
            self.obj_func
        )

        return new_solution



    def update_route_values(self, route, position, request):
        pass
    

    def get_attr_relation_reader_heuristic(self):
        return {}