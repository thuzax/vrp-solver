import time
import copy
import random
from pprint import pprint

from src.solution_methods import *
from src.route_classes import *
from src.objects_managers import *
from src.solution_classes import *
from src import file_log
from src import execution_log


from src.solvers import SolverPDPTW
from src.solution_check import solution_check, get_solution_check_complete_data


class SolverDPDPTW(SolverPDPTW):

    def __init__(self):
        super().__init__()


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fixed_requests = None


    def insert_fixed(self, solution):
        for route_pos, route_fixed in enumerate(self.fixed_requests):
            route = Route()
            solution.add_route(route)
            for pair in route_fixed:
                insertion = InsertionOperator().get_best_insertion_in_route( 
                    route,
                    pair,
                    self.obj_func,
                    self.constraints
                )
                insert_pos, new_route, insert_cost = insertion
                InsertionOperator().insert_request_in_solution(
                    solution,
                    pair,
                    insert_pos,
                    new_route,
                    route_pos,
                    self.obj_func
                )
                route = new_route

        return solution



    def construct(self, parameters):
        file_log.add_info_log("Starting construction")
        solution = Solution()
        
        solution = self.insert_fixed(solution)
        parameters["requests_set"] -= solution.requests()
        
        solution = self.construction.solve(solution, parameters)
        
        file_log.add_info_log("Finished construction")

        obj_value = self.obj_func.get_solution_cost(solution)
        routes_cost = self.obj_func.get_routes_sum_cost(
            solution.routes
        )

        solution.set_objective_value(obj_value)
        solution.set_routes_cost(routes_cost)

        self.best_solution = solution.copy()
        
        if (
            not solution_check(
                self.best_solution, 
                self.constraints, 
                self.obj_func
            )
        ):
            file_log.add_warning_log("Could not construct feasible solution")
            execution_log.warning_log(
                "Could not construct feasible solution"
            )
            self.best_solution = None
            return self.best_solution
        
        # Log
        message = "Solution after " + self.construction_name + "\n"
        file_log.add_solution_log(self.best_solution, message)

        print(solution)
        return solution
        


    def solve(self):
        file_log.add_info_log("Starting solver.")
        heuristic_start = time.time()

        requests_set = set(self.requests)
        parameters = {
            "requests_set" : requests_set
        }

        solution = self.construct(parameters)


        file_log.add_info_log("Starting metaheuristic")
        new_solution = self.metaheuristic.solve(solution, parameters)
        self.best_solution = new_solution.copy()
        file_log.add_info_log("Finished metaheuristic")
        

        obj_value = self.obj_func.get_solution_cost(self.best_solution)
        routes_cost = self.obj_func.get_routes_sum_cost(
            self.best_solution.routes
        )

        self.best_solution.set_objective_value(obj_value)
        self.best_solution.set_routes_cost(routes_cost)
        
        # Log
        message = "Solution after " + self.metaheuristic_name + "\n"
        file_log.add_solution_log(self.best_solution, message)
        
        heuristic_end = time.time()
        exec_time = heuristic_end - heuristic_start
        
        # self.print_best_solution()
        # self.print_solution_verification(self.best_solution, exec_time)

        return self.best_solution


    def update_heuristics_data(self):
        self.construction = HeuristicsObjects().get_by_name(
            self.construction_name
        )

        self.metaheuristic = HeuristicsObjects().get_by_name(
            self.metaheuristic_name
        )


    def get_attr_relation_reader_solver(self):
        read_solv_attr_rela = {
            "input_name" : "output_name",
            "vertices" : "vertices",
            "requests" : "requests",
            "number_of_requests" : "number_of_requests",
            "fixed" : "fixed_requests"
        }
        return read_solv_attr_rela