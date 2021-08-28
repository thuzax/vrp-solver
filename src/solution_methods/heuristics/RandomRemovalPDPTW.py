
import random

from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.heuristics.RandomRemoval import RandomRemoval

class RandomRemovalPDPTW(RandomRemoval):

    def __init__(self):
        super().__init__("Random Removal PDPTW")

        self.vertices = None
        self.time_matrix = None
        self.depot = None
        self.number_of_requests = None


    def update_solution_requests_costs(
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
        for key, value in dict_costs.items():
            solution.set_request_cost(key, value)




    def update_route_values(self, route, position, request):
        pickup_position, delivery_position = position
        
        for i in range(pickup_position, route.size()):
            arrival_time = (
                self.calculate_arrival_time(route, i)
            )
            occupied_capacity = (
                self.calculate_demand_on_vertex(route, i)
            )

            route.arrival_times[i] = arrival_time
            route.capacity_occupations[i] = occupied_capacity


    def calculate_demand_on_vertex(self, route, position):
        route_order = route.get_order()
        vertex_id = route_order[position]

        if (position == 0):
            return self.vertices[vertex_id].demand
        
        previous_occ = route.capacity_occupations[position-1] 

        demand = (
            previous_occ
            + self.vertices[vertex_id].demand
        )

        return demand


    def calculate_arrival_time(self, route, position):
        route_order = route.get_order()
        vertex_id = route_order[position]
        
        if (position == 0):
            return self.time_matrix[self.depot][vertex_id]

        
        previous_id = route_order[position-1]
        
        previous_start_service = route.arrival_times[position-1]
        previous_tw = self.vertices[previous_id].time_window

        if (previous_start_service < previous_tw[0]):
            previous_start_service = previous_tw[0]

        previous_service_time = self.vertices[previous_id].service_time
        
        travel_time = self.time_matrix[previous_id][vertex_id]

        arrival_time = (
            previous_start_service 
            + previous_service_time 
            + travel_time
        )

        return arrival_time


    @staticmethod
    def get_attr_relation_reader_heuristic():
        rela_reader_heur = {
            "vertices" : "vertices",
            "time_matrix" : "time_matrix",
            "number_of_requests" : "number_of_requests",
            "depot" : "depot"
        }
        return rela_reader_heur

