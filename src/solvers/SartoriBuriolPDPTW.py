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


class SartoriBuriolPDPTW(SolverClass):

    def __init__(self):
        super().__init__("Sartori and Buriol 2020 algorithm")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.vertices = None
        self.number_of_requests = None
        self.requests = None

        self.construction_name = None
        self.construction = None
        self.local_searches = None
        self.local_searches_order = None

    def execute_local_search(
        self, 
        solution, 
        local_search_pos,
        parameters
    ):
        start = time.time()
        solution = self.local_searches[local_search_pos].solve(
            solution, 
            parameters
        )
        solution.set_objective_value(self.obj_func.get_solution_cost(solution))
        solution.set_routes_total_cost(
            self.obj_func.get_routes_sum_cost(solution.routes)
        )
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        if (solution_check(solution, self.constraints, self.obj_func)):
            print(
                "SOLUTION IS OK AFTER", 
                self.local_searches_order[local_search_pos]
            )
        else:
            print(
                get_solution_check_complete_data(
                    solution, 
                    self.constraints, 
                    self.obj_func
                )
            )
        print(
            "obj_func, obj_route: ", 
            solution.cost(), 
            ",",
            solution.routes_cost()
        )
        print(
            self.local_searches_order[local_search_pos],
            "time:", 
            time.time() - start
        )
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

        return solution


    def construct_initial_solution(self):
        insertion_requests = set(self.requests)
        # print(self.requests)
        routes = []
        last_size = len(insertion_requests)
        
        solution = Solution()
        inserted = True
        heuristic_start = time.time()
        start = time.time()
        while (inserted and len(insertion_requests) > 0):
            solution.add_route(Route())
            parameters = {}

            parameters["requests"] = insertion_requests
            parameters["k"] = 1

            solution = self.construction.solve(solution, parameters)
            insertion_requests -= solution.requests()
            if (last_size == len(insertion_requests)):
                routes.pop()
                inserted = False
            
        self.remaining_requests_set = insertion_requests
        self.inserted_requests_set = (
            set(self.requests)
            - self.remaining_requests_set
        )

        solution.set_objective_value(self.obj_func.get_solution_cost(solution))
        solution.set_routes_total_cost(
            self.obj_func.get_routes_sum_cost(solution.routes)
        )
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if (solution_check(solution, self.constraints, self.obj_func)):
            print("SOLUTION IS OK AFTER", self.construction_name)
        else:
            print(
                get_solution_check_complete_data(
                    solution, 
                    self.constraints, 
                    self.obj_func
                )
            )
        print(
            "obj_func, obj_route: ", 
            solution.cost(), 
            ",",
            solution.routes_cost()
        )

        print(self.construction_name, "time:", time.time() - start)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # print(solution)
        parameters = {}
        parameters["remaining_requests"] = self.remaining_requests_set
        solution = self.execute_local_search(solution, 0, parameters)
        # print(solution)
        parameters = {}
        parameters["remaining_requests"] = self.remaining_requests_set
        solution = self.execute_local_search(solution, 1, parameters)

        # print(solution)
        # parameters = {}
        # parameters["requests"] = set(self.requests)
        # parameters["routes_pool"] = [route for route in solution.routes]
        # solution = self.execute_local_search(solution, 2, parameters)
        
        # print(solution)
        parameters = {}
        parameters["n_perturb"] = 50
        solution = self.execute_local_search(solution, 3, parameters)

        # print(solution)
        print("Total time:", time.time() - heuristic_start)


        self.remaining_requests_set = (
            set(self.requests)
            - solution.requests()
        )
        print("REMAINING: " + str(self.remaining_requests_set))

        return solution

    def solve(self):
        solution = self.construct_initial_solution()
        print("..........................................")
        print("..........................................")
        print("FINAL VERIFICATION")
        print("..........................................")
        print("..........................................")
        print(solution)
        print(
            get_solution_check_complete_data(
                solution, 
                self.constraints, 
                self.obj_func
            )
        )


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
            "input_name" : "alternative_output_name",
            "vertices" : "vertices",
            "requests" : "requests",
            "number_of_requests" : "number_of_requests"
        }
        return read_solv_attr_rela