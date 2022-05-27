
import copy
import time
from src.solution_methods.construction_heuristics.BasicGreedy import BasicGreedy

from src.solution_check import get_solution_check_complete_data, solution_check
from src.solution_methods.heuristics.WKRegret import WKRegret
from src.solution_methods.heuristics.KRegret import KRegret
from src.route_classes.Route import Route
from src.solution_methods.SolutionMethod import SolutionMethod


class BasicGreedyLimitedHeterogeneousFleet(BasicGreedy):
    
    def __init__(self):
        super().__init__("Basic Greedy Heuristic")
    
    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fleet = None


    def get_insertion_heuristic(self):
        return super().get_insertion_heuristic()

    def solve(self, solution, parameters):
        
        insertion_heuristic = self.get_insertion_heuristic()
        start = time.time()
        insertion_requests = copy.deepcopy(parameters["requests_set"])
        last_size = len(insertion_requests)
        inserted = True
        if (len(solution.routes()) > 0):
            parameters = {}
            parameters["requests_set"] = insertion_requests
            parameters["k"] = 1
            solution = insertion_heuristic.solve(solution, parameters)
            insertion_requests -= solution.requests()

        exec_time = time.time() - start
        solution.set_objective_value(self.obj_func.get_solution_cost(solution))
        solution.set_routes_cost(
            self.obj_func.get_routes_sum_cost(solution.routes())
        )
        

        return solution


    def get_attr_relation_reader_heuristic(self):
        needed_data = super().get_attr_relation_reader_heuristic()
        needed_data["fleet"] = "fleet"
        return needed_data
