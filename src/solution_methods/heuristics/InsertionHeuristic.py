import bisect

from abc import ABCMeta, abstractmethod

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

    @abstractmethod
    def get_route_feasible_insertions(self, route, request):
        pass


    def get_best_insertion_in_route(self, route, request):
        feasible_positions = self.get_route_feasible_insertions(route, request)

        best_route = None
        best_insertion_position = None

        for position, route in feasible_positions:
            if (self.obj_func.route_is_better(route, best_route)):
                best_route = route
                best_insertion_position = position

        return (
            best_insertion_position,
            best_route
        )


    def get_best_insertions_in_routes(self, request, routes, best_routes_ids):
        request_k_routes = []
        request_k_insertions = []
        request_k_costs = []
        route_ids = []

        for i in best_routes_ids:
            route = routes[i]
            position, new_route = (
                self.get_best_insertion_in_route(route, request)
            )
            if (new_route is None):
                cost = self.non_insertion_cost
                new_route = None
            else:
                cost = new_route.cost()
            
            order_position = bisect.bisect(
                request_k_costs, 
                cost
            )
        
            request_k_costs.insert(order_position, cost)
            request_k_insertions.insert(order_position, position)
            request_k_routes.insert(order_position, new_route)
            route_ids.insert(order_position, i)

        return (
            route_ids,
            request_k_routes,
            request_k_insertions,
            request_k_costs
        )


    def verify_if_insertion_is_possible(self, routes):
        can_be_inserted = False
        i = 0
        while ((i < len(routes)) and (not can_be_inserted)):
            route = routes[i]
            if (route is not None):
                can_be_inserted = True
            i += 1
            continue
            
        return can_be_inserted




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
