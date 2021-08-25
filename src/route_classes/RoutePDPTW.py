
import math
import copy
import numpy

from src.route_classes import Route


class RoutePDPTW(Route):

    def __init__(self):
        super().__init__("Route PDPTW")


    def initialize_class_attributes(self):
        self.arrival_times = []
        self.capacity_occupations = []
        


    def insert_vertex(self, position, vertex):
        self.vertices_order.insert(position, vertex)
        self.vertices_set.add(vertex)

        self.arrival_times.insert(position, -1)
        self.capacity_occupations.insert(position, 0)


    def insert(self, insert_position, request):
        pickup_pos, delivery_pos = insert_position
        pickup, delivery = request

        self.insert_vertex(pickup_pos, pickup)
        self.insert_vertex(delivery_pos, delivery)


    def remove(self, vertex):
        self.vertices_set.remove(vertex)
        self.vertices_order.remove(vertex)


    def cost(self):
        return super().cost()


    def number_of_requests(self):
        return int(self.size()/2)


    def copy(self):
        copy_route = Route()

        copy_route.vertices_order = copy.copy(self.vertices_order)
        copy_route.vertices_set = copy.copy(self.vertices_set)
        
        copy_route.route_cost = copy.copy(self.route_cost)

        copy_route.arrival_times = copy.copy(self.arrival_times)
        copy_route.capacity_occupations = copy.copy(self.capacity_occupations)

        return copy_route


    def __str__(self):
        text = "Route: " + str(self.vertices_order) + "\n"
        text += "Arrivals: " + str(self.arrival_times) + "\n"
        text += "Capacities: " + str(self.capacity_occupations) + "\n"
        text += "Cost: " + str(self.route_cost) + "\n"
        return text


    @staticmethod
    def get_attr_relation_reader_route():
        reader_route_attr_rela = {
        }
        
        return reader_route_attr_rela
