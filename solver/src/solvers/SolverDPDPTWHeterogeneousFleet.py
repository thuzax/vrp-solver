import time
import copy

from src.solution_methods import *
from src.route_classes import *
from src.objects_managers import *
from src.solution_classes import *
from src import file_log
from src import execution_log
from src.objects_managers import ConstraintsObjects


from src.solvers import SolverDPDPTW
from src.solution_check import solution_check, get_solution_check_complete_data


class SolverDPDPTWHeterogeneousFleet(SolverDPDPTW):

    def __init__(self):
        super().__init__()

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fleet = None

    def create_routes(self):
        routes = []
        for fleet_item in self.fleet.values():
            for i in range(fleet_item["size"]):
                routes.append(Route(fleet_item["types"]))
    
        return routes

    def insert_fixed(self, solution):
        routes = self.create_routes()
        for route_pos, route_fixed_dict in enumerate(self.fixed_requests):
            route_requests = route_fixed_dict["requests"]
            route_order = route_fixed_dict["route"]
            route_returned = None
            
            
            fleet_type_data = self.fleet[route_fixed_dict["fleet_type"]]
            vehic_type_needed = fleet_type_data["types"]
            
            i = 0
            while (route_returned is None):
                route_attendance_type = routes[i].get_attendance_type()
                if (route_attendance_type != vehic_type_needed):
                    i += 1
                    continue
                solution.add_route(routes[i])
                route_returned = self.insert_fixed_route_in_solution(
                    routes[i],
                    solution,
                    route_pos,
                    route_order,
                    route_requests
                )
                routes.pop(i)
                
                i += 1
            route_returned.set_start_position(route_fixed_dict["start"])
        
        for route in routes:
            solution.add_route(route)
        
        solution.set_objective_value(self.obj_func.get_solution_cost(solution))
        # print(solution)
        # self.print_solution_verification(solution, 0)
        return solution


    def get_attr_relation_reader_solver(self):
        read_solv_attr_rela = {
            "input_name": "output_name",
            "vertices": "vertices",
            "requests": "requests",
            "number_of_requests": "number_of_requests",
            "fixed_routes_dict": "fixed_requests",
            "fleet" : "fleet"
        }
        return read_solv_attr_rela
