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
            old_route = new_solution.get_request_route(request_to_move)
            remov_request_pos_in_route = old_route.index(request_to_move)
            route_pos = new_solution.find_route_position_by_id(
                old_route.get_id()
            )

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

            # Try to find feasible insertions in random routes
            feasible_positions_and_routes = []
            new_route_pos = None
            routes = [route for route in new_solution.routes]
            while(len(routes) > 0 and not found_shift):

                new_route_pos = random.randint(0, len(routes)-1)
                route = routes.pop(new_route_pos)

                if (route.get_id() == old_route.get_id()):
                    new_route_pos += 1
                    continue
            
                feasible_positions_and_routes = (
                    InsertionOperator().get_route_feasible_insertions(
                        route,
                        request_to_move,
                        self.obj_func,
                        self.constraints
                    )
                )
            
                if (len(feasible_positions_and_routes) > 0):
                    found_shift = True
                    continue
            

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

        # Divide the feasible insertions of the random request into 
        # position where inserted and route after insertion
        insertion_positions = []
        routes_after_insertion = []
        for feasible_insertion in feasible_positions_and_routes:
            positions, routes = feasible_insertion
            insertion_positions.append(positions)
            routes_after_insertion.append(routes)
        
        # Remove the shift to same place
        k = 0
        found_old_route = False
        while (k < len(routes_after_insertion) and not found_old_route):
            route_after_insertion = routes_after_insertion[k]
            if (route_after_insertion.get_id() == old_route.get_id()):
                if (insertion_positions[k] == remov_request_pos_in_route):
                    found_old_route = True
                    continue
            k += 1


        # Choose a random new route
        route_inserted_pos = random.randint(0, len(routes_after_insertion)-1)
        route_inserted = routes_after_insertion[route_inserted_pos]
        
        route_pos_in_sol = new_solution.find_route_position_by_id(
            route_inserted.get_id()
        )

        position_insertion = insertion_positions[route_inserted_pos]

        # Add the route in solution
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