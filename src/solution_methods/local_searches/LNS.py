
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
import time
import copy
import random
from src import exceptions
from src import file_log
from src.solution_methods.local_searches.LocalSearch import LocalSearch


class LNS(LocalSearch):

    def __init__(self):
        super().__init__("LNS")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        
        self.max_time = None
        self.max_time_without_improv = None
        
        self.max_it = None
        self.max_it_without_improv = None

        self.stop_criteria = None
        self.stop_parameters = None

        self.k_min = None 
        self.k_max = None
        self.b_min = None 
        self.b_max = None

        self.kregret = None
        self.shaw_removal = None
        self.random_removal = None
        self.worst_removal = None

        self.removals_probabilities = None


    def get_current_best_solution(self):
        return super().get_current_best_solution()


    def solve(self, solution, parameters):
        copy_solution = solution.copy()
        copy_solution.set_objective_value(
            self.obj_func.get_solution_cost(copy_solution)
        )
        copy_solution.set_routes_cost(
            self.obj_func.get_routes_sum_cost(copy_solution.routes)
        )
        
        self.best_solution = copy_solution

        extra_requests = copy.deepcopy(parameters["remaining_requests"])
        all_requests = extra_requests.union(copy_solution.requests())


        self.stop_parameters = {}
        self.stop_parameters["begin_time"] = time.time()
        self.stop_parameters["it"] = 0
        self.stop_parameters["it_last_improv"] = 0
        self.stop_parameters["time_last_it"] = 0
        self.stop_parameters["time_last_improv"] = 0
        improved = False

        while (not self.stop_criteria_fulfilled()):
            new_solution = copy_solution.copy()

            # Removal 
            n_b_max = int(
                self.b_max * len(all_requests)
            )
            if (n_b_max < self.b_min):
                n_b_max = self.b_min
            
            b = random.randint(self.b_min, n_b_max)
            new_solution = self.remove_from_solution(
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
            new_solution = self.reinsert_requests(
                extra_requests, 
                k, 
                new_solution
            )


            new_solution.set_objective_value(
                self.obj_func.get_solution_cost(new_solution)
            )

            # Acceptance
            self.stop_parameters["it"] += 1
            self.stop_parameters["time_last_it"] = time.time()
            accepted = (
                self.solution_is_feasible(new_solution) 
                and self.accept(new_solution)
            )
            if (
                accepted 
                and 
                self.obj_func.solution_is_better(
                        new_solution, 
                        self.best_solution
                )
            ):
                self.best_solution = new_solution
                self.stop_parameters["time_last_improv"] = time.time()
                self.stop_parameters["it_last_improv"] = (
                    self.stop_parameters["it"]
                )
                improved = True



            if (accepted):
                copy_solution = new_solution
    
            extra_requests = all_requests - copy_solution.requests()

        message = "LNS" + "\n"
        message += "IT: " +  str(self.stop_parameters["it"])
        message += "\n"
        message += "Exec Time: "
        message += str(
            self.stop_parameters["time_last_it"] 
            - self.stop_parameters["begin_time"]
        )
        message += "\n"
        message += "Improved\n" if improved else ""

        file_log.add_solution_log(self.best_solution, message)
        
        return self.best_solution


    def update_route_values(self, route, position, request):
        super().update_route_values(route, position, request)


    def reinsert_requests(self, requests, k, solution):
        parameters = {}
        parameters["k"] = k
        if (k >= solution.number_of_routes()):
            parameters["k"] = solution.number_of_routes()-1
        
        parameters["requests_set"] = requests
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


    def stop_criteria_fulfilled(self):
        if (self.stop_criteria == "time"):
            begin_time = self.stop_parameters["begin_time"]
            time_last_improv = self.stop_parameters["time_last_improv"]
            time_last_it = self.stop_parameters["time_last_it"]
            return self.time_stop_criteria_fulfilled(
                begin_time,
                time_last_improv, 
                time_last_it
            )
        elif(self.stop_criteria == "iterations"):
            it_last_improv = self.stop_parameters["it_last_improv"]
            it = self.stop_parameters["it"]
            return self.it_stop_criteria_fulfilled(
                it_last_improv,
                it
            )

        raise exceptions.WrongOrUndefinedStopCriteria(self.__name__)


    def time_stop_criteria_fulfilled(self, 
        begin_time,
        time_last_improv, 
        time_last_it
    ):
        if (time_last_improv - begin_time >= self.max_time_without_improv):
            return True

        if (time_last_it - begin_time >= self.max_time):
            return True

        return False


    def it_stop_criteria_fulfilled(self, it_last_improv, it):
        if (it_last_improv >= self.max_it_without_improv):
            return True

        if (it >= self.max_it):
            return True

        return False


    def get_attr_relation_reader_heuristic(self):
        rela_reader_heur = super().get_attr_relation_reader_heuristic()
        return rela_reader_heur


    def define_local_searches_operators(self, op_dict):
        return super().define_local_searches_operators(op_dict)