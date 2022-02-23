import random
import copy
import numpy


from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator

class RandomExchange(SolutionMethod):

    def __init__(self):
        super().__init__("Random Shift")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def try_to_exchange(self, request_1, route_1, request_2, route_2):
        new_route_1 = RemovalOperator().try_to_remove(
            route_1,
            request_1, 
            self.obj_func,
            self.constraints
        )

        if (new_route_1 is None):
            return None

        new_route_2 = RemovalOperator().try_to_remove(
            route_2,
            request_2, 
            self.obj_func,
            self.constraints
        )

        if (new_route_2 is None):
            return None

        insert_pos_1, insert_route_1, insert_cost_1 = (
            InsertionOperator().get_best_insertion_in_route(
                new_route_1,
                request_2,
                self.obj_func,
                self.constraints
            )
        )

        if (insert_pos_1 is None or insert_route_1 is None):
            return None
        

        insert_pos_2, insert_route_2, insert_cost_2 = (
            InsertionOperator().get_best_insertion_in_route(
                new_route_2,
                request_1,
                self.obj_func,
                self.constraints
            )
        )

        if (insert_pos_2 is None or insert_route_2 is None):
            return None
        
        return (
            (insert_pos_1, insert_route_1),
            (insert_pos_2, insert_route_2)
        )



    def solve(self, solution, parameters):
        new_solution = solution.copy()

        first_route_pos = None
        second_route_pos = None

        past_moves = set()
        max_number_of_moves = 0
        for i in range(len(new_solution.routes())-1):
            route_i_size = new_solution.routes()[i].number_of_requests()
            for j in range(i+1, len(new_solution.routes())):
                route_j_size = new_solution.routes()[j].number_of_requests()
                max_number_of_moves += route_i_size * route_j_size

        exchange_found = False
        while(len(past_moves) < max_number_of_moves and not exchange_found):
            first_route_pos, second_route_pos = tuple(random.sample(
                [i for i in range(len(new_solution.routes()))],
                2
            ))

            first_route = new_solution.routes()[first_route_pos]
            second_route = new_solution.routes()[second_route_pos]
            if (first_route.size() == 0):
                continue
            if (second_route.size() == 0):
                continue
            
            first_request = random.choice(
                list(first_route.requests())
            )
            second_request = random.choice(
                list(second_route.requests())
            )

            move_1 = (
                first_route_pos,
                first_request,
                second_route_pos,
                second_request
            )
            move_2 = (
                second_route_pos,
                second_request,
                first_route_pos,
                first_request
            )

            if (move_1 in past_moves or move_2 in past_moves):
                continue

            past_moves.add(move_1)

            exchanged_pos_routes = self.try_to_exchange(
                first_request, 
                first_route.copy(), 
                second_request, 
                second_route.copy()
            )

            if (exchanged_pos_routes is None):
                continue
            
            exchange_found = True
        
        if (not exchange_found):
            return solution.copy()

        first_route_insert_pos, first_new_route = exchanged_pos_routes[0]
        second_route_insert_pos, second_new_route = exchanged_pos_routes[1]

        first_route_after_remotion = RemovalOperator().try_to_remove(
            first_route,
            first_request,
            self.obj_func,
            self.constraints
        )

        RemovalOperator().remove_request_from_solution(
            new_solution,
            first_request,
            first_route.index(first_request),
            first_route_after_remotion,
            first_route_pos,
            self.obj_func
        )


        second_route_after_remotion = RemovalOperator().try_to_remove(
            second_route,
            second_request,
            self.obj_func,
            self.constraints
        )

        RemovalOperator().remove_request_from_solution(
            new_solution,
            second_request,
            second_route.index(second_request),
            second_route_after_remotion,
            second_route_pos,
            self.obj_func
        )

        new_solution = InsertionOperator().insert_request_in_solution(
            new_solution,
            second_request,
            first_route_insert_pos,
            first_new_route,
            first_route_pos,
            self.obj_func
        )

        new_solution = InsertionOperator().insert_request_in_solution(
            new_solution,
            first_request,
            second_route_insert_pos,
            second_new_route,
            second_route_pos,
            self.obj_func
        )


        return new_solution



    def get_current_best_solution(self):
        return super().get_current_best_solution()

    def update_route_values(self, route, position, request):
        pass

    def get_attr_relation_reader_heuristic(self):
        return {}