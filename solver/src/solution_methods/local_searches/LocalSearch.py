from abc import ABCMeta, abstractmethod

from numpy import copy
from src.solution_methods.SolutionMethod import SolutionMethod

class LocalSearch(SolutionMethod, metaclass=ABCMeta):

    def __init__(self, name):
        super().__init__(name)

    @abstractmethod
    def initialize_class_attributes(self):
        super().initialize_class_attributes()

        self.local_operators_names = None
        self.local_operators = None

        self.acceptance_algorithm_data = None
        self.acceptance_algorithm = None


    @abstractmethod
    def stop_criteria_fulfilled(self):
        pass


    @abstractmethod
    def define_local_searches_operators(self, op_dict):
        self.local_operators = {}
        for key, value in op_dict.items():
            self.local_operators[key] = value

    def accept(self, new_solution, parameters=None):
        return self.acceptance_algorithm.accept(
            new_solution, 
            self.obj_func, 
            parameters
        )