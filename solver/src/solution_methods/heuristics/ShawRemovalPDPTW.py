from abc import ABCMeta, abstractmethod

import random
from src.solution_methods.heuristics.ShawRemoval import ShawRemoval

class ShawRemovalPDPTW(ShawRemoval):

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

        route_pos_r_1, route_r_1 = solution.get_request_route(r_1)
        route_pos_r_2, route_r_2 = solution.get_request_route(r_2)

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


    def get_attr_relation_reader_heuristic(self):
        rela_reader_heur = {
            "distance_matrix" : "distance_matrix",
            "demands" : "demands",
            "time_windows" : "time_windows",
        }
        return rela_reader_heur

    def update_route_values(self, route, position, request):
        return super().update_route_values(route, position, request)


    def get_exception_requests(self, solution):
        return super().get_exception_requests(solution)