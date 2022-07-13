from abc import ABCMeta, abstractmethod

import random

from src.solution_methods.heuristics.ShawRemovalPDPTW import ShawRemovalPDPTW
from src import file_log

class ShawRemovalDPDPTW(ShawRemovalPDPTW):

    def __init__(self):
        super().__init__()


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fixed_routes_dict = None


    def get_attr_relation_reader_heuristic(self):
        rela_reader_heur = {
            "distance_matrix" : "distance_matrix",
            "demands" : "demands",
            "time_windows" : "time_windows",
            "fixed_routes_dict" : "fixed_routes_dict"
        }
        return rela_reader_heur


    def update_route_values(self, route, position, request):
        return super().update_route_values(route, position, request)


    def choose_one_random_request_to_remove(self, requests, solution):
        possible_requests = (
            set(requests) - set(self.get_exception_requests(solution))
        )
        if (len(possible_requests) == 0):
            return None
        request = random.choice(list(possible_requests))
        return request


    def get_exception_requests(self, solution):
        exception_requests = []
        for fixed_route_dict in self.fixed_routes_dict:
            for request in fixed_route_dict["requests"]:
                if (solution.get_request_route(request) is None):
                    continue
                req_route_pos, req_route = solution.get_request_route(request)
                position_request = req_route.index(request)
                if (position_request[0] <= fixed_route_dict["start"]):
                    exception_requests.append(request)
                # exception_requests.append(request)

        return exception_requests

