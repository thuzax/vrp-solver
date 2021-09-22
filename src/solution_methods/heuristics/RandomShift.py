import random
import copy


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

        requests_copy = copy.deepcopy(new_solution.requests())
        
        request_to_move = None
        old_route = None
        remov_request_pos_in_route = None
        route_pos = None
        new_route = None
        found_shift = False
        # Find feasible shift
        while (not found_shift and len(requests_copy) > 0):
            # Choose request to move and get its route
            request_to_move = random.choice(list(requests_copy))
            requests_copy.remove(request_to_move)

            route_pos, old_route = (
                new_solution.get_request_route(request_to_move)
            )
            
            remov_request_pos_in_route = old_route.index(request_to_move)

            # remove request
            new_route = RemovalOperator().try_to_remove(
                new_solution.routes[route_pos],
                request_to_move,
                self.obj_func,
                self.constraints
            )

            if (new_route is None):
                continue
            
            new_solution = RemovalOperator().remove_request_from_solution(
                new_solution,
                request_to_move,
                remov_request_pos_in_route,
                new_route,
                route_pos,
                self.obj_func
            )

            routes_to_insert = [
                new_solution.routes[i]
                for i in range(len(new_solution.routes))
                if i != route_pos
            ]

            # Try to find feasible insertions in random routes
            feasible_positions_and_routes = (
                InsertionOperator().get_all_feasible_insertions_from_routes(
                    request_to_move,
                    routes_to_insert,
                    self.obj_func,
                    self.constraints
                )
            )
            
            if (len(feasible_positions_and_routes) > 0):
                found_shift = True
            
            if (not found_shift):
                new_solution = InsertionOperator().insert_request_in_solution(
                    new_solution,
                    request_to_move,
                    old_route.index(request_to_move),
                    old_route,
                    route_pos,
                    self.obj_func
                )

        # If there is no feasible shift for any request, return None
        if (not found_shift):
            return solution.copy()


        # Otherwise make a shift of the chosen random request to a random route
        # Choose a random new route
        feasible_insertion = random.choice(feasible_positions_and_routes)
        insertion_pos, route_inserted, insert_cost = feasible_insertion

        old_route_identifying = (
            InsertionOperator().get_route_id_value_before_inserted(
                route_inserted,
                request_to_move
            )
        )

        route_pos_in_sol = (
            new_solution.find_route_position_by_identifying_value(
                old_route_identifying
            )
        )


        # Add the route in solution
        InsertionOperator().insert_request_in_solution(
            new_solution,
            request_to_move,
            insertion_pos,
            route_inserted,
            route_pos_in_sol,
            self.obj_func
        )

        return new_solution



    def update_route_values(self, route, position, request):
        pass
    

    def get_attr_relation_reader_heuristic(self):
        return {}