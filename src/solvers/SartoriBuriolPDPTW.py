import copy
from pprint import pprint

from src.heuristics import *
from src.route_classes import *
from src.objects_managers import *
from src.solvers.SovlerClass import SolverClass


class SartoriBuriolPDPTW(SolverClass):

    def __init__(self):
        super().__init__("Sartori and Buriol 2020 algorithm")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.vertices = None
        self.distance_matrix = None
        self.time_matrix = None
        self.capacity = None
        self.demands = None
        self.services_times = None
        self.time_windows = None
        self.planning_horizon = None
        self.time_windows_size = None
        self.depot = None
        self.pickups_ids = None
        self.deliveries_ids = None
        self.number_of_requests = None
        self.requests = None

        self.remaining_requests_set = None

        self.construction_name = None
        self.construction = None
        self.local_searches = None
        self.local_searches_order = None


    def construct_initial_solution(self):
        insertion_requests = set(self.requests)
        routes = []
        last_size = len(insertion_requests)
        inserted = True
        while (inserted and len(insertion_requests) > 0):
            routes.append(Route())
            parameters = {}
            parameters["routes"] = routes
            parameters["requests"] = insertion_requests
            parameters["k"] = 1

            self.construction.solve(parameters)
            if (last_size == len(insertion_requests)):
                routes.pop()
                inserted = False

        self.remaining_requests_set = insertion_requests
        self.inserted_request = (
            set(self.requests)
            - self.remaining_requests_set
        )

        return routes

    def solve(self):
        solution_routes = self.construct_initial_solution()

        if (not self.solution_is_feasible(solution_routes)):
            print("Solution not feasible")
            for route in solution_routes:
                if (not self.route_is_feasible(route)):
                    print("Route not feasible: ")
                    print(route)
            return
        
        print("=========================================================")
        print("Requests inserted: " + str(self.inserted_request))
        print("Requests remaining: " + str(self.remaining_requests_set))
        print("-----------------------Routes----------------------------")
        for route in solution_routes:
            print(route)
        
        print("Solution Cost:")
        print(self.obj_func.get_solution_cost(solution_routes))
        print("Solution is Feasible")


    def update_heuristics_data(self):
        self.construction = HeuristicsObjects().get_by_name(
            self.construction_name
        )

        self.local_searches = []
        for local_search_name in self.local_searches_order:
            local_search = HeuristicsObjects().get_by_name(local_search_name)
            self.local_searches.append(local_search)


    def write_file(self):
        return super().write_file()


    def get_attr_relation_reader_solver(self):
        read_solv_attr_rela = {
            "vertices" : "vertices",
            "distance_matrix" : "distance_matrix",
            "time_matrix" : "time_matrix",
            "capacity" : "capacity",
            "demands" : "demands",
            "services_times" : "services_times",
            "time_windows" : "time_windows",
            "planning_horizon" : "planning_horizon",
            "time_windows_size" : "time_windows_size",
            "depot" : "depot",
            "pickups" : "pickups_ids",
            "deliveries" : "deliveries_ids",
            "requests" : "requests",
            "number_of_requests" : "number_of_requests"
        }
        return read_solv_attr_rela