import random
import copy
import numpy
import time
from numpy.lib.function_base import insert


from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator

class ModBiasedShift(SolutionMethod):

    def __init__(self):
        super().__init__("Random Shift")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.mi = None

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

        insertion_costs = []

        for position, route_after, insert_cost in feasible_positions_and_routes:
            cost = self.obj_func.route_additional_route_cost_after_insertion(
                route_after,
                position,
                route_after.get_request_by_position(position)
            )
            insertion_costs.append(cost)

        a = time.time()
        partition_k = int(self.mi * len(insertion_costs))
        if (partition_k == 0):
            partition_k = 1

        best_indices = [i for i in range(len(insertion_costs))]
        
        if (len(insertion_costs) > partition_k):
            costs_array = numpy.array(insertion_costs)
            best_indices = numpy.argpartition(
                costs_array, 
                partition_k
            )
            best_indices = best_indices[:partition_k].tolist()

        feasible_insert_pos = random.randint(0, len(best_indices)-1)

        feasible_insertion = feasible_positions_and_routes[feasible_insert_pos]
        insertion_pos, route_inserted = feasible_insertion

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
        rela = {}
        return rela