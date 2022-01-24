
import math
import copy
import numpy

from src.route_classes import Route
from src.route_classes import RoutePDPTW


class RouteDPDPTW(RoutePDPTW):

    def __init__(self):
        super().__init__()

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fixed_requests = set()
        self.last_fixed_pickup = 0


    def insert_in_route(self, insert_position, request, params=None):
        
        pickup_pos, delivery_pos = insert_position
        pickup, delivery = request
        self.requests_set.add(request)
        
        ## REMOVER E ESTUDAR POSSIBILIDADE DE USAR ROTA PDPTW
        if (params is not None and params["is_fixed"]):
            pickup_pos = self.last_fixed_pickup
            self.last_fixed_pickup += 1
            self.fixed_requests.add(request)
            

        self.insert_vertex(pickup_pos, pickup)
        self.insert_vertex(delivery_pos, delivery)



    def pop_from_route(self, position):
        request = self.get_request_by_position(position)

        pickup_pos, delivery_pos = position

        pickup = self.pop_vertex(pickup_pos)
        delivery = self.pop_vertex(delivery_pos-1)

        self.requests_set.remove((pickup, delivery))

        return (pickup, delivery)


    def is_fixed(self, request):
        if (request in self.fixed):
            return True
        
        return False


    def copy_route_to(self, route_copy):
        route_copy.arrival_times = copy.deepcopy(self.arrival_times)
        route_copy.capacity_occupations = copy.deepcopy(
            self.capacity_occupations
        )
        route_copy.fixed_requests = copy.deepcopy(self.fixed_requests)
        route_copy.last_fixed_pickup = self.last_fixed_pickup


    def __str__(self):
        text = "Route: " + str(self.vertices_order) + "\n"
        text += "Arrivals: " + str(self.arrival_times) + "\n"
        text += "Capacities: " + str(self.capacity_occupations) + "\n"
        text += "Cost: " + str(self.route_cost) + "\n"
        text += "Fixeds: "  + str(self.fixed_requests) + "\n"
        return text


    @staticmethod
    def get_attr_relation_reader_route():
        reader_route_attr_rela = {
        }
        
        return reader_route_attr_rela
