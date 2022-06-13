
import copy
import time
from src.solution_methods.heuristics.FirstInsertionUnlimitedFleet import FirstInsertionUnlimitedFleet
from src.solution_methods.heuristics.FirstInsertion import FirstInsertion

from src.solution_check import get_solution_check_complete_data, solution_check
from src.solution_methods.heuristics.WKRegret import WKRegret
from src.solution_methods.heuristics.KRegret import KRegret
from src.route_classes.Route import Route
from src.solution_methods.SolutionMethod import SolutionMethod


class BasicGreedy(SolutionMethod):
    
    def __init__(self, *args, **kwargs):
        if (len(args) > 0):
            super().__init__(args[0])
        else:
            super().__init__("Basic Greedy Heuristic")
    
    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.insertion_heuristic_code = None


    def get_insertion_heuristic(self):
        if (self.insertion_heuristic_code == "wkr"):
            return WKRegret()
        
        if (self.insertion_heuristic_code == "kr"):
            return KRegret()

        if (self.insertion_heuristic_code == "fi"):
            return FirstInsertion()
        
        if (self.insertion_heuristic_code == "fiuf"):
            return FirstInsertionUnlimitedFleet()


    def insert_only_in_last_route(self):
        if (self.insertion_heuristic_code == "wkr"):
            return True
        
        if (self.insertion_heuristic_code == "kr"):
            return True

        if (self.insertion_heuristic_code == "fi"):
            return True
        
        if (self.insertion_heuristic_code == "fiuf"):
            return True


    def solve(self, solution, parameters_inp):
        
        insertion_heuristic = self.get_insertion_heuristic()
        start = time.time()
        insertion_requests = copy.deepcopy(parameters_inp["requests_set"])
        last_size = len(insertion_requests)
        inserted = True

        if (len(solution.routes()) > 0):
            parameters = {}
            parameters["requests_set"] = insertion_requests
            parameters["k"] = 1
            solution = insertion_heuristic.solve(solution, parameters)
            insertion_requests -= solution.requests()
        
        solution.add_route(Route())

        
        while (inserted and len(insertion_requests) > 0):

            last_size = len(insertion_requests)

            parameters = {}

            parameters["requests_set"] = insertion_requests
            parameters["k"] = 1
            parameters["route"] = None
            if (self.insert_only_in_last_route()):
                parameters["route"] = solution.number_of_routes()-1
            solution = insertion_heuristic.solve(solution, parameters)
            insertion_requests -= solution.requests()
            if (last_size == len(insertion_requests)):
                solution.remove_route(-1)
                inserted = False
            
            solution.add_route(Route())
        
        for i, route in enumerate(solution.routes()):
            if (route.empty()):
                solution.remove_route(i)
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
        return {}

