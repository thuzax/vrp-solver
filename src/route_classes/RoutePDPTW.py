
import math
import copy
import numpy

from src.route_classes import Route


class RoutePDPTW(Route):

    planning_horizon = None
    time_windows_size = None

    time_matrix = None
    services_times = None
    time_windows = None
    demands = None
    capacity = None

    def __init__(self):
        if (not hasattr(self, "name")):
            super().__init__("Route PDPTW")
            self.arrival_times = []
            self.total_demand_on_vertices = []
            self.total_cost = 0




    def update_route_values(self, initial_position, final_position):
        for i in range(initial_position, final_position):
            self.arrival_times[i] = (
                self.calculate_arrival_time(i, self.vertices_order[i])
            )
            self.total_demand_on_vertices[i] = (
                self.calculate_demand_on_vertex(i, self.vertices_order[i])
            )


    def calculate_demand_on_vertex(self, position, vertex):
        if (position == 0):
            return self.demands[vertex]
        
        demand = (
            self.total_demand_on_vertices[position-1] 
            + self.demands[vertex]
        )

        return demand


    def calculate_arrival_time(self, position, vertex):
        if (position == 0):
            return 0
        
        previous_position = position - 1
        previous = self.vertices_order[previous_position]

        previous_start_service = self.arrival_times[position-1]
        if (previous_start_service < self.time_windows[previous][0]):
            previous_start_service = self.time_windows[previous][0]


        previous_service_time = self.services_times[previous]
        
        travel_time = self.time_matrix[previous][vertex]


        arrival_time = (
            previous_start_service 
            + previous_service_time 
            + travel_time
        )

        return arrival_time

    def insert_vertex(self, position, vertex):
        self.vertices_order.insert(position, vertex)
        self.vertices_set.add(vertex)
        self.arrival_times.insert(position, -1)
        self.total_demand_on_vertices.insert(position, -1)
        self.update_route_values(position, self.size())


    def insert(self, insert_position, request, obj_func):
        pickup_pos, delivery_pos = insert_position
        pickup, delivery = request

        self.insert_vertex(pickup_pos, pickup)
        self.insert_vertex(delivery_pos, delivery)
        
        self.total_cost += obj_func.request_inserted_additional_cost(
            self,
            insert_position, 
            request
        )


    def remove(self, vertex):
        self.vertices_set.remove(vertex)
        self.vertices_order.remove(vertex)


    def respect_planning_horizon(self):
        last_vertex = self.vertices_order[-1]
        journey_end = self.arrival_times[-1] + self.services_times[last_vertex]
        if (journey_end > self.planning_horizon):
            return False
        return True


    def respect_time_windows(self, start_point=0):
        for i in range(start_point, self.size()):
            vertex = self.vertices_order[i]
            end_tw = self.time_windows[vertex][1]
            if (self.arrival_times[i] > end_tw):
                return False

        # if arrival_time < start_tw, vehicle waits
        return True


    def respect_capacity(self, start_point=0):
        
        for i in range(start_point, len(self.total_demand_on_vertices)):
            if (
                self.total_demand_on_vertices[i] > self.capacity
                or self.total_demand_on_vertices[i] < 0
            ):
                return False
        
        if (self.total_demand_on_vertices[-1] > self.capacity):
            return False
        
        return True


    def is_feasible(self, start_point=0):
        if (not self.respect_planning_horizon()):
            return False

        if (not self.respect_time_windows(start_point)):
            return False

        if (not self.respect_capacity(start_point)):
            return False

        return True


    def cost(self):
        return self.total_cost


    def number_of_requests(self):
        return int(self.size()/2)


    def copy(self):
        copy_route = Route()
        copy_route.arrival_times = copy.copy(self.arrival_times)
        copy_route.total_cost = copy.copy(self.total_cost)
        copy_route.vertices_order = copy.copy(self.vertices_order)
        copy_route.vertices_set = copy.copy(self.vertices_set)
        copy_route.total_demand_on_vertices = (
            copy.copy(self.total_demand_on_vertices)
        )

        return copy_route


    def __str__(self):
        text = "Route: " + str(self.vertices_order) + "\n"
        text += "Arrival Time: " + str(self.arrival_times) + "\n"
        text += "Demands: " + str(self.total_demand_on_vertices) + "\n"
        text += "Cost: " + str(self.total_cost) + "\n"
        return text


    @staticmethod
    def get_attr_relation_solver_route():
        solver_route_attr_rela = {
            "planning_horizon" : "planning_horizon",
            "time_windows_size" : "time_windows_size",
            "time_matrix" : "time_matrix",
            "services_times" : "services_times",
            "time_windows" : "time_windows",
            "demands" : "demands",
            "capacity" : "capacity"
        }
        
        return solver_route_attr_rela
