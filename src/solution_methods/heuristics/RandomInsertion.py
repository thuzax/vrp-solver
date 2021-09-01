from abc import ABCMeta

import random

from src.solution_methods.heuristics.InsertionHeuristic import InsertionHeuristic


class RandomInsertion(InsertionHeuristic, metaclass=ABCMeta):

    def __init__(self, name):
        super().__init__(name)


    def solve(self, solution, parameters):
        new_solution = solution.copy()
        requests = parameters["requests"]

        for request in requests:
            feasible_insertions = self.get_all_feasible_insertions_from_routes(
                request, 
                new_solution.routes
            )

            insertion_positions = []
            routes_after_insertion = []
            for route_feasible_insertions in feasible_insertions:
                if (len(route_feasible_insertions) > 0):
                    positions, routes = tuple(zip(*route_feasible_insertions))
                    insertion_positions += list(positions)
                    routes_after_insertion += list(routes)
            
            if (len(routes_after_insertion) <= 0):
                continue

            new_route_pos = random.randint(0, len(routes_after_insertion)-1)
            new_route = routes_after_insertion[new_route_pos]
            inserted_pos = insertion_positions[new_route_pos]
            
            old_route_pos = new_solution.find_route_position_by_id(
                new_route.get_id()
            )
            
            new_solution.set_route(old_route_pos, new_route)
            new_solution.add_request(request)
            self.update_solution_requests_costs_after_insertion(
                new_solution, 
                new_route, 
                inserted_pos,
                request
            )

        return new_solution


    def try_to_insert(self, route, position, request):
        return super().try_to_insert(route, position, request)
