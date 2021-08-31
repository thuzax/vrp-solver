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

        copy_route.route_cost += (
            self.obj_func.route_reduced_route_cost_before_removal(
                route,
                position, 
                request
            )
        )


        if (self.route_is_feasible(copy_route)):
            return copy_route


    def update_solution_requests_costs_after_removal(
        self, 
        solution, 
        route, 
        position, 
        request
    ):
        route_order = route.get_order()
        # Positions from where the request were removed
        pick_pos, deli_pos = position
        pick_next_pos = pick_pos
        deli_next_pos = deli_pos - 1

        pick_prev_pair = (-1, -1)
        if (pick_next_pos > 0):
            pick_prev_id = route_order[pick_next_pos-1]
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
        if (deli_next_pos < route.size()):
            deli_next_id = route_order[deli_next_pos]
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
            if (pick_next_pos < route.size()):
                pick_next_id = route_order[pick_next_pos]
                pick_next_pair = (
                    pick_next_id,
                    pick_next_id + self.number_of_requests
                )
                if (pick_next_id > self.number_of_requests):
                    pick_next_pair = (
                        pick_next_id - self.number_of_requests,
                        pick_next_id
                    )
            if (deli_next_pos > 0):
                deli_prev_id = route_order[deli_next_pos-1]
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
