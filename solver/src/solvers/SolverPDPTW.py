import time

from src.solution_methods import *
from src.route_classes import *
from src.objects_managers import *
from src.solution_classes import *
from src import file_log
from src import execution_log
from src import exceptions


from src.solvers import SolverClass
from src.solution_check import solution_check, get_solution_check_complete_data


class SolverPDPTW(SolverClass):

    def __init__(self):
        super().__init__("Solver for PDPTW")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.vertices = None
        self.number_of_requests = None
        self.requests = None


    def construct(self, parameters, start_time):
        file_log.add_info_log("Starting construction")
        execution_log.info_log("Starting construction")
        solution = Solution()
        solution = self.construction.solve(solution, parameters)
        
        file_log.add_info_log("Finished construction")
        execution_log.info_log("Finished construction")

        obj_value = self.obj_func.get_solution_cost(solution)
        routes_cost = self.obj_func.get_routes_sum_cost(
            solution.routes()
        )

        solution.set_objective_value(obj_value)
        solution.set_routes_cost(routes_cost)

        self.best_solution = solution.copy()

        message = self.construction.name + "\n"
        message += "Exec Time: " + str(time.time() - start_time)
        message += "\n"
        file_log.add_solution_log(self.best_solution, message)
        
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
            file_log.add_info_log(
                get_solution_check_complete_data(
                    self.best_solution, 
                    self.constraints, 
                    self.obj_func
                )
            )
            self.best_solution = None
            return self.best_solution
        
        # Log
        message = "Solution after " + self.construction_name + "\n"
        file_log.add_solution_log(self.best_solution, message)

        return solution
        


    def solve(self):
        file_log.add_info_log("Starting solver.")
        execution_log.info_log("Starting solver.")
        heuristic_start = time.time()

        requests_set = set(self.requests)
        parameters = {
            "requests_set" : requests_set
        }

        solution = self.construct(parameters, heuristic_start)
        if (solution is None):
            return None
        file_log.add_info_log("Starting metaheuristic")
        execution_log.info_log("Starting metaheuristic")
        new_solution = self.metaheuristic.solve(solution, parameters)
        self.best_solution = new_solution.copy()
        file_log.add_info_log("Finished metaheuristic")
        execution_log.info_log("Finished metaheuristic")
        

        obj_value = self.obj_func.get_solution_cost(self.best_solution)
        routes_cost = self.obj_func.get_routes_sum_cost(
            self.best_solution.routes()
        )

        self.best_solution.set_objective_value(obj_value)
        self.best_solution.set_routes_cost(routes_cost)
        
        # Log
        message = "Solution after " + self.metaheuristic_name + "\n"
        file_log.add_solution_log(self.best_solution, message)
        
        heuristic_end = time.time()
        exec_time = heuristic_end - heuristic_start
        
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
            "number_of_requests" : "number_of_requests"
        }
        return read_solv_attr_rela