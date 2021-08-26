
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

        self.arrival_times.insert(position, -1)
        self.capacity_occupations.insert(position, 0)


    def insert(self, insert_position, request):
        pickup_pos, delivery_pos = insert_position
        pickup, delivery = request
        self.requests_set.add(request)

        self.insert_vertex(pickup_pos, pickup)
        self.insert_vertex(delivery_pos, delivery)


    def index(self, request):
        pickup, delivery = request
        
        position_pickup = self.vertices_order.index(pickup)
        position_delivery = self.vertices_order.index(delivery)

        return (position_pickup, position_delivery)


    def pop_vertex(self, position):
        
        vertex_id = self.vertices_order.pop(position)
        self.arrival_times.pop(position)
        self.capacity_occupations.pop(position)


        return vertex_id



    def pop(self, position):
        pickup_pos, delivery_pos = position

        pickup = self.pop_vertex(pickup_pos)
        delivery = self.pop_vertex(delivery_pos-1)

        self.requests_set.remove((pickup, delivery))

        return (pickup, delivery)


    def remove(self, request):
        pickup_pos, delivery_pos = self.index(request)

        self.pop_vertex(pickup_pos)
        self.pop_vertex(delivery_pos)




    def cost(self):
        return super().cost()


    def number_of_requests(self):
        return int(self.size()/2)


    def copy(self):
        copy_route = Route()

        copy_route.vertices_order = copy.deepcopy(self.vertices_order)
        copy_route.requests_set = copy.deepcopy(self.requests_set)
        
        copy_route.route_cost = copy.deepcopy(self.route_cost)

        copy_route.arrival_times = copy.deepcopy(self.arrival_times)
        copy_route.capacity_occupations = copy.deepcopy(
            self.capacity_occupations
        )

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
