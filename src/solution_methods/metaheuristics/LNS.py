
import time
import copy
import random
from src import exceptions
from src.solution_methods.metaheuristics.LocalSearch import LocalSearch

class LNS(LocalSearch):
    

    def __init__(self):
        super().__init__("LNS")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        
        self.begin_time = None

        self.max_time = None
        self.max_time_without_improv = None
        
        self.max_it = None
        self.max_it_without_improv = None

        self.stop_criteria = None

        self.k_min = None 
        self.k_max = None
        self.b_min = None 
        self.b_max = None

        self.kregret = None
        self.shaw_removal = None
        self.random_removal = None
        self.worst_removal = None

        self.removals_probabilities = None



    def solve(self, solution, parameters):
        solution.set_objective_value(self.obj_func.get_solution_cost(solution))
        solution.set_routes_total_cost(
            self.obj_func.get_routes_sum_cost(solution.routes)
        )
        
        best_solution = solution

        extra_requests = copy.deepcopy(parameters["remaining_requests"])
        all_requests = extra_requests.union(solution.requests())

        self.begin_time = time.time()

        stop_parameters = {}
        stop_parameters["it"] = 0
        stop_parameters["it_last_improv"] = 0
        stop_parameters["time_last_it"] = 0
        stop_parameters["time_last_improv"] = 0
        
        while (not self.stop_criteria_fulfilled(stop_parameters)):
            new_solution = solution.copy()

            # Removal 
            n_b_max = int(
                self.b_max * len(all_requests)
            )
            if (n_b_max < self.b_min):
                n_b_max = self.b_min
            
            b = random.randint(self.b_min, n_b_max)
            solution = self.remove_from_solution(
                b, 
                new_solution
            )

            removed_requests = all_requests - new_solution.requests()

            new_solution.set_objective_value(
                self.obj_func.get_solution_cost(new_solution)
            )
            
            # Reinsertion
            extra_requests = extra_requests.union(removed_requests)
            
            k = random.randint(self.k_min, self.k_max)
            solution = self.reinsert_requests(
                extra_requests, 
                k, 
                new_solution
            )

            extra_requests = all_requests - new_solution.requests()

            new_solution.set_objective_value(
                self.obj_func.get_solution_cost(new_solution)
            )
            
            # Acceptance
            stop_parameters["it"] += 1
            stop_parameters["time_last_it"] = time.time()

            if (self.obj_func.solution_is_better(new_solution, best_solution)):
                best_solution = new_solution
                stop_parameters["time_last_improv"] = time.time()
                stop_parameters["it_last_improv"] = stop_parameters["it"]
                print(
                    "IMPROVED", 
                    best_solution.cost(), 
                    best_solution.routes_cost()
                )

            
            if (self.accept(new_solution)):
                solution = new_solution
        
        print("LNS iteartion: ", stop_parameters["it"])
        return best_solution


    def accept(self, new_solution):
        return super().accept(new_solution)


    def update_route_values(self, route, position, request):
        super().update_route_values(route, position, request)


    def reinsert_requests(self, requests, k, solution):
        parameters = {}
        parameters["k"] = k
        if (k >= solution.number_of_routes()):
            parameters["k"] = solution.number_of_routes()-1
        
        parameters["requests"] = requests
        solution = (
            self.local_operators["KRegret"].solve(solution, parameters)
        )

        return solution


    def remove_from_solution(self, b, solution):
        keys = list(self.removals_probabilities.keys())
        probabilities = [self.removals_probabilities[key] for key in keys]
        weights = [p/sum(probabilities) for p in probabilities]
        operator_name = random.choices(keys, weights=weights)[0]
        operator = self.local_operators[operator_name]
        parameters = {}
        parameters["b"] = b
        new_solution = operator.solve(solution, parameters)
        return new_solution


    def stop_criteria_fulfilled(self, stop_parameters):
        if (self.stop_criteria == "time"):
            time_last_improv = stop_parameters["time_last_improv"]
            time_last_it = stop_parameters["time_last_it"]
            return self.time_stop_criteria_fulfilled(
                time_last_improv, 
                time_last_it
            )
        elif(self.stop_criteria == "iterations"):
            it_last_improv = stop_parameters["it_last_improv"]
            it = stop_parameters["it"]
            return self.it_stop_criteria_fulfilled(
                it_last_improv,
                it
            )

        raise exceptions.WrongOrUndefinedStopCriteria(self.__name__)


    def time_stop_criteria_fulfilled(self, time_last_improv, time_last_it):
        if (time_last_improv - self.begin_time >= self.max_time_without_improv):
            return True
        if (time_last_it - self.begin_time >= self.max_time):
            return True
        return False


    def it_stop_criteria_fulfilled(self, it_last_improv, it):
        if (it_last_improv >= self.max_it_without_improv):
            return True
        if (it >= self.max_it):
            return True
        return False


    @staticmethod
    def get_attr_relation_reader_heuristic():
        rela_reader_heur = LocalSearch.get_attr_relation_reader_heuristic()
        return rela_reader_heur


    def define_local_searches_operators(self, op_dict):
        self.local_operators = {}
        self.local_operators["ShawRemoval"] = op_dict["ShawRemoval"]
        self.local_operators["RandomRemoval"] = op_dict["RandomRemoval"]
        self.local_operators["WorstRemoval"] = op_dict["WorstRemoval"]
        self.local_operators["KRegret"] = op_dict["KRegret"]