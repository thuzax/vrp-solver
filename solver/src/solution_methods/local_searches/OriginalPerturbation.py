
import random
import time
from src import file_log
from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.local_searches.LocalSearch import LocalSearch


class OriginalPerturbation(LocalSearch):
    
    def __init__(self):
        super().__init__("Original Perturbation")
    
    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.perturb_probabilities = None


    def solve(self, solution, parameters):
        new_solution = solution.copy()
        self.best_solution = new_solution.copy()
        start_time = time.time()
        
        number_of_perturbations = parameters["n_perturb"]
        for i in range(number_of_perturbations):

            keys = list(self.perturb_probabilities.keys())
            probabilities = [self.perturb_probabilities[key] for key in keys]
            weights = [p/sum(probabilities) for p in probabilities]

            perturb_name = random.choices(keys, weights=weights)[0]
            perturb_operator = self.local_operators[perturb_name]
            new_solution = perturb_operator.solve(new_solution, {})

            new_is_better = self.obj_func.solution_is_better(
                new_solution, 
                self.best_solution
            )
            if (new_is_better):
                self.best_solution = new_solution
        
        if (
            self.solution_is_feasible(new_solution) 
            and self.accept(new_solution)
        ):
            return new_solution

        return solution


    def stop_criteria_fulfilled(self):
        super().stop_criteria_fulfilled()

    def get_current_best_solution(self):
        return super().get_current_best_solution()

    def update_route_values(self, route, position, request):
        return super().update_route_values(route, position, request)

    def get_attr_relation_reader_heuristic(self):
        return super().get_attr_relation_reader_heuristic()

    def define_local_searches_operators(self, op_dict):
        return super().define_local_searches_operators(op_dict)