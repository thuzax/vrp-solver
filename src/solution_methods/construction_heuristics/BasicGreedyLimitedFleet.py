
import copy
import time

from src.solution_check import get_solution_check_complete_data, solution_check
from src.solution_methods.heuristics.WKRegret import WKRegret
from src.solution_methods.heuristics.KRegret import KRegret
from src.route_classes.Route import Route
from src.solution_methods.SolutionMethod import SolutionMethod


class BasicGreedyLimitedFleet(SolutionMethod):
    
    def __init__(self):
        super().__init__("Basic Greedy Heuristic")
    
    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.insertion_heuristic_code = None
        self.fleet_size = None


    def get_insertion_heuristic(self):
        if (self.insertion_heuristic_code == "wkr"):
            return WKRegret()
        
        if (self.insertion_heuristic_code == "kr"):
            return KRegret()


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
        
        
        number_of_routes_to_add = self.fleet_size - len(solution.routes())
        for i in range(number_of_routes_to_add):
            solution.add_route(Route())

        
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


    def print_solution_verification(self, solution, exec_time):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if (solution_check(solution, self.constraints, self.obj_func)):
            print("SOLUTION IS OK AFTER", self.name)
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

        print(self.name, "time:", exec_time)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # self.add_routes_to_pool(solution.routes())


    def get_current_best_solution(self):
        return super().get_current_best_solution()

    def update_route_values(self, route, position, request):
        pass
    

    def get_attr_relation_reader_heuristic(self):
        return {
            "fleet_size" : "fleet_size"
        }

