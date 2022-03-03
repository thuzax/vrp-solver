import random
from src.solution_methods.acceptance_heuristics.AcceptanceHeuristic import AcceptanceHeuristic
from src.GenericClass import GenericClass


class AcceptBetterOrWithProbability(AcceptanceHeuristic):

    def __init__(self):
        super().__init__("Accept Better Or With Probability")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def accept(self, new_solution, obj_func, parameters):
        best_solution = parameters["best_solution"]
        probability = parameters["probability"]

        new_is_better = obj_func.solution_is_better(new_solution, best_solution)

        if (new_is_better):
            return True
        
        if (random.random() < probability):
            return True

        return False


    def get_attr_relation_reader_accept_heuri(self):
        return {}