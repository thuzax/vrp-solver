
import math
import copy
import numpy

from src.route_classes import Route
from src.route_classes import RouteClass


class RoutePDPTW(RouteClass):

    def __init__(self):
        super().__init__("Route PDPTW")


    def initialize_class_attributes(self):
        self.arrival_times = []
        self.capacity_occupations = []
        


    def insert_vertex(self, position, vertex):
        self.vertices_order.insert(position, vertex)

        self.arrival_times.insert(position, -1)
        self.capacity_occupations.insert(position, 0)


    def insert_in_route(self, insert_position, request):
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



    def pop_from_route(self, position):
        pickup_pos, delivery_pos = position

        pickup = self.pop_vertex(pickup_pos)
        delivery = self.pop_vertex(delivery_pos-1)

        self.requests_set.remove((pickup, delivery))

        return (pickup, delivery)



    def remove(self, request):
        position = self.index(request)
        self.pop((position))


    def get_request_by_position(self, position):
        pick_pos, deli_pos = position

        return (self.vertices_order[pick_pos], self.vertices_order[deli_pos])


    def get_arrival_time(self, request):
        pick_pos, deli_pos = self.index(request)
        arrival_times = (
            self.arrival_times[pick_pos],
            self.arrival_times[deli_pos]
        )
        return arrival_times


    def cost(self):
        return super().cost()


    def number_of_requests(self):
        return int(self.size()/2)


    def copy_route_to(self, route_copy):
        route_copy.arrival_times = copy.deepcopy(self.arrival_times)
        route_copy.capacity_occupations = copy.deepcopy(
            self.capacity_occupations
        )


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
