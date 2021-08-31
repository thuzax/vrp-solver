from abc import ABCMeta, abstractmethod

from numpy import copy
from src.solution_methods.SolutionMethod import SolutionMethod

class InsertionHeuristic(SolutionMethod, metaclass=ABCMeta):

    def __init__(self, name):
        super().__init__(name)


    @abstractmethod
    def try_to_insert(self, route, position, request):
        copy_route = route.copy()
        copy_route.insert(position, request)

        self.update_route_values(copy_route, position, request)
        copy_route.route_cost += (
            self.obj_func.route_additional_route_cost_after_insertion(
                copy_route,
                position, 
                request
            )
        )


        if (self.route_is_feasible(copy_route)):
            return copy_route


    def update_solution_requests_costs_after_insertion(
        self, 
        solution, 
        route, 
        position, 
        request
    ):
        route_order = route.get_order()
        pick_pos, deli_pos = position
        pick_prev_pair = (-1, -1)
        if (pick_pos > 0):
            pick_prev_id = route_order[pick_pos-1]
            pick_prev_pair = (
                pick_prev_id,
                pick_prev_id + self.number_of_requests
            )
            if (pick_prev_id > self.number_of_requests):
                pick_prev_pair = (
                    pick_prev_id - self.number_of_requests,
                    pick_prev_id
                )
        
        deli_next_pair = (-1, -1)
        if (deli_pos < route.size()-1):
            deli_next_id = route_order[deli_pos+1]
            deli_next_pair = (
                deli_next_id,
                deli_next_id + self.number_of_requests
            )
            if (deli_next_id > self.number_of_requests):
                deli_next_pair = (
                    deli_next_id - self.number_of_requests,
                    deli_next_id
                )
        pick_next_pair = (-1, -1)
        deli_prev_pair = (-1, -1)
        if (pick_pos < deli_pos-1):
            pick_next_id = route_order[pick_pos+1]
            pick_next_pair = (
                pick_next_id,
                pick_next_id + self.number_of_requests
            )
            if (pick_next_id > self.number_of_requests):
                pick_next_pair = (
                    pick_next_id - self.number_of_requests,
                    pick_next_id
                )
            
            deli_prev_id = route_order[deli_pos-1]
            deli_prev_pair = (
                deli_prev_id,
                deli_prev_id + self.number_of_requests
            )
            if (deli_prev_id > self.number_of_requests):
                deli_prev_pair = (
                    deli_prev_id - self.number_of_requests,
                    deli_prev_id
                )
        
        pairs = (
            set([
                request,
                pick_prev_pair,
                deli_next_pair,
                pick_next_pair,
                deli_prev_pair
            ])
        )
        pairs.discard((-1, -1))

        dict_costs = {}
        for pair in pairs:
            pos_pair = route.index(pair)
            dict_costs[pair] = self.obj_func.get_request_cost_in_route(
                route,
                pos_pair,
                pair
            )
        
        for pair, cost in dict_costs.items():
            solution.set_request_cost(pair, cost)
