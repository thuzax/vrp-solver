import copy
import random
from pprint import pprint
from time import sleep, time

from src.solution_methods import *
from src.route_classes import *
from src.objects_managers import *
from src.solution_classes import *

from src.solvers.SolverClass import SolverClass


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


    def construct_initial_solution(self):
        insertion_requests = set(self.requests)
        routes = []
        last_size = len(insertion_requests)
        
        solution = Solution()
        inserted = True
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
        if (self.solution_check(solution, self.constraints, self.obj_func)):
            print("SOLUTION IS OK AFTER INSERTION")
        else:
            print(
                self.get_solution_check_complete_data(
                    solution, 
                    self.constraints, 
                    self.obj_func
                )
            )
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # print(solution)
        parameters["remaining_requests"] = self.remaining_requests_set
        solution = self.local_searches[0].solve(
            solution, 
            parameters
        )
        solution.set_objective_value(self.obj_func.get_solution_cost(solution))
        solution.set_routes_total_cost(
            self.obj_func.get_routes_sum_cost(solution.routes)
        )


        self.remaining_requests_set = (
            set(self.requests)
            - solution.requests()
        )
        print("REMAINING: " + str(self.remaining_requests_set))

        return solution

    def solve(self):
        solution = self.construct_initial_solution()
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(solution)
        print(
            self.get_solution_check_complete_data(
                solution, 
                self.constraints, 
                self.obj_func
            )
        )


    def calculate_requests_total_cost(self, solution, obj_func):
        obj_requests_cost = 0
        for route in solution.routes:
            for request in route.get_requests_set():
                obj_requests_cost += (
                    obj_func.get_request_cost_in_route(
                        route, 
                        route.index(request),
                        request
                    )
                )
        return obj_requests_cost


    def calculate_routes_total_cost(self, solution, obj_func):
        routes_obj_value = 0
        for route in solution.routes:
            routes_obj_value += obj_func.get_route_cost(route) 
        return routes_obj_value


    def constraints_check(self, solution, constraints):
        for constraint in constraints:
            if (not constraint.solution_is_feasible(solution)):
                return False
        return True


    def objective_function_value_check(self, solution, obj_func):
        obj_value = obj_func.get_solution_cost(solution)
        if (obj_value != solution.cost()):
            return False

        return True

    def routes_total_value_check(self, solution, obj_func):
        routes_obj_value = self.calculate_routes_total_cost(solution, obj_func)
        if (routes_obj_value != solution.routes_cost()):
            return False
        return True


    def requests_costs_check(self, solution, obj_func):
        requests_cost = 0
        for request_cost in solution.requests_costs().values():
            requests_cost += request_cost

        obj_requests_cost = (
            self.calculate_requests_total_cost(solution, obj_func)
        )

        route_total_cost = self.calculate_routes_total_cost(solution, obj_func)
        if (obj_requests_cost != requests_cost):
            return False

        return True


    def solution_check(self, solution, constraints, obj_func):
        solution_ok = (
            self.constraints_check(solution, constraints)
            and self.objective_function_value_check(solution, obj_func)
            and self.requests_costs_check(solution, obj_func)
        )
        
        return solution_ok



    def get_solution_check_complete_data(self, solution, constraints, obj_func):
        text = ""
        text += "====================================" + "\n"
        text += "Constraints verification: " + "\n"
        for constraint in constraints:
            if (constraint.solution_is_feasible(solution)):
                text += constraint.name + " OK" + "\n"
            else:
                text += constraint.name + " NOT OK FOR THESE ROUTES" + "\n"
                for route in solution.routes:
                    if (not constraint.route_is_feasible(route)):
                        text += str(route) + "\n"

        text += "====================================" + "\n"

        text += "Obj Func verification: " + "\n"
        
        obj_value = obj_func.get_solution_cost(solution)
        
        if (obj_value == solution.cost()):
            text += "SOLUTION COST OK" + "\n"
        else:
            text += "SOLUTION COST NOT OK:" + "\n"
            text += str(solution.cost()) + "\n"
            text += str(obj_value) + "\n"
        text += "------------------------------------" + "\n"
        
        
        routes_obj_value = self.calculate_routes_total_cost(solution, obj_func)
        
        if (routes_obj_value == solution.routes_cost()):
            text += "ROUTES TOTAL COST OK" + "\n"
        else:
            text += "ROUTES TOTAL COST NOT OK:" + "\n"
            text += str(solution.routes_cost()) + "\n"
            text += str(routes_obj_value) + "\n"
        text += "------------------------------------" + "\n"

        requests_cost = 0
        for request_cost in solution.requests_cost_dict.values():
            requests_cost += request_cost
        
        obj_requests_cost = (
            self.calculate_requests_total_cost(solution, obj_func)
        )

        if (obj_requests_cost == requests_cost):
            text += "REQUESTS TOTAL COST OK" + "\n"
        else:
            text += "REQUESTS TOTAL COST NOT OK:" + "\n"
            text += str(obj_requests_cost) + "\n"
            text += str(requests_cost) + "\n"
        text += "------------------------------------" + "\n"

        return text



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
            "requests" : "requests",
            "number_of_requests" : "number_of_requests"
        }
        return read_solv_attr_rela