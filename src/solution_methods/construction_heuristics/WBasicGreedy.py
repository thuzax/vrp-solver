
import copy
import time

from src.solution_check import get_solution_check_complete_data, solution_check
from src.solution_methods.heuristics.WKRegret import WKRegret
from src.route_classes.Route import Route
from src.solution_classes.Solution import Solution
from src.solution_methods.SolutionMethod import SolutionMethod


class WBasicGreedy(SolutionMethod):
    
    def __init__(self):
        super().__init__("Basic Greedy Heuristic")
    
    def initialize_class_attributes(self):
        super().initialize_class_attributes()

    def solve(self, parameters):
        start = time.time()
        insertion_requests = copy.deepcopy(parameters["requests_set"])
        routes = []
        last_size = len(insertion_requests)
        
        solution = Solution()
        inserted = True
        while (inserted and len(insertion_requests) > 0):
            last_size = len(insertion_requests)

            solution.add_route(Route())
            parameters = {}

            parameters["requests_set"] = insertion_requests
            parameters["k"] = 1
            solution = WKRegret().solve(solution, parameters)
            insertion_requests -= solution.requests()
            if (solution.has_empty_route()):
                solution.routes.pop()
                inserted = False
            
            
        exec_time = time.time() - start
        solution.set_objective_value(self.obj_func.get_solution_cost(solution))
        solution.set_routes_cost(
            self.obj_func.get_routes_sum_cost(solution.routes)
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
        # self.add_routes_to_pool(solution.routes)


    def get_current_best_solution(self):
        return super().get_current_best_solution()

    def update_route_values(self, route, position, request):
        pass
    

    def get_attr_relation_reader_heuristic(self):
        return {}

