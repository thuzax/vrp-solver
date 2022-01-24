from abc import ABCMeta, abstractmethod

import random
from src.solution_methods.heuristics.ShawRemovalPDPTW import ShawRemovalPDPTW

class ShawRemovalDPDPTW(ShawRemovalPDPTW):

    def __init__(self):
        super().__init__()


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fixed_routes = None


    def get_attr_relation_reader_heuristic(self):
        rela_reader_heur = {
            "distance_matrix" : "distance_matrix",
            "demands" : "demands",
            "time_windows" : "time_windows",
            "fixed" : "fixed_routes"
        }
        return rela_reader_heur


    def update_route_values(self, route, position, request):
        return super().update_route_values(route, position, request)


    def choose_one_random_request_to_remove(self, requests):
        possible_requests = set(requests) - set(self.get_exception_requests())
        request = random.choice(list(possible_requests))
        return request


    def get_exception_requests(self):
        exception_requests = []
        for fixed_route in self.fixed_routes:
            for request in fixed_route:
                exception_requests.append(request)

        return exception_requests

