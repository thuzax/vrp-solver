from abc import ABCMeta, abstractmethod

import random
from src.solution_methods.heuristics.ShawRemoval import ShawRemoval

from src.solution_methods.SolutionMethod import SolutionMethod

class ShawRemovalPDPTW(ShawRemoval, metaclass=ABCMeta):

    def __init__(self):
        super().__init__("Shaw Removal PDPTW")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.distance_matrix = None
        self.time_windows = None
        self.demands = None

        self.relatedness_measure = None

        self.phi = None
        self.qui = None
        self.psi = None


        self.vertices = None
        self.time_matrix = None
        self.depot = None
        self.number_of_requests = None


    def calculate_request_relatedness_measure(self, solution, r_1, r_2):
        p_1, d_1 = r_1
        p_2, d_2 = r_2
        dist_relation = (
            (
                self.distance_matrix[p_1][p_2] 
                + self.distance_matrix[p_2][p_1]
                + self.distance_matrix[d_1][d_2]
                + self.distance_matrix[d_2][d_1]
            ) / 2
        )

        route_r_1 = solution.get_request_route(r_1)
        route_r_2 = solution.get_request_route(r_2)

        arrival_times_r_1 = route_r_1.get_arrival_time(r_1)
        arrival_times_r_2 = route_r_2.get_arrival_time(r_2)

        pick_1_arrival, deli_1_arrival = arrival_times_r_1
        pick_2_arrival, deli_2_arrival = arrival_times_r_2

        time_relation = (
            abs(pick_1_arrival - pick_2_arrival)
            + abs(deli_1_arrival - deli_2_arrival)
        )

        capacity_relation = abs(self.demands[p_1] - self.demands[p_2])

        relatedness_measure = (
            self.phi * dist_relation
            + self.qui * time_relation
            + self.psi * capacity_relation
        )

        return relatedness_measure


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
            "distance_matrix" : "distance_matrix",
            "demands" : "demands",
            "time_windows" : "time_windows",
            "vertices" : "vertices",
            "time_matrix" : "time_matrix",
            "number_of_requests" : "number_of_requests",
            "depot" : "depot"
        }
        return rela_reader_heur

