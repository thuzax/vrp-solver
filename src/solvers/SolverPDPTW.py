import time
import copy
import random
from pprint import pprint

from src.solution_methods import *
from src.route_classes import *
from src.objects_managers import *
from src.solution_classes import *

from src.solvers.SolverClass import SolverClass
from src.solution_check import solution_check, get_solution_check_complete_data


class SolverPDPTW(SolverClass):

    def __init__(self):
        super().__init__("Solver for PDPTW")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.vertices = None
        self.number_of_requests = None
        self.requests = None

    def solve(self):
        heuristic_start = time.time()
        requests_set = set(self.requests)
        parameters = {
            "requests_set" : requests_set
        }
        
        solution = self.construction.solve(parameters)
        self.best_solution = solution.copy()
        self.best_solution = self.metaheuristic.solve(solution, parameters)
        heuristic_end = time.time()
        exec_time = heuristic_end - heuristic_start
        
        self.print_solution_verification(self.best_solution, exec_time)

        return self.best_solution


    def update_heuristics_data(self):
        self.construction = HeuristicsObjects().get_by_name(
            self.construction_name
        )

        self.metaheuristic = HeuristicsObjects().get_by_name(
            self.metaheuristic_name
        )


    def write_file(self):
        return super().write_file()


    def get_attr_relation_reader_solver(self):
        read_solv_attr_rela = {
            "input_name" : "alternative_output_name",
            "vertices" : "vertices",
            "requests" : "requests",
            "number_of_requests" : "number_of_requests"
        }
        return read_solv_attr_rela