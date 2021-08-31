
from abc import ABCMeta, abstractmethod

from src import exceptions
from src.objects_managers import HeuristicsObjects
from src.GenericClass import GenericClass


class SolutionMethod(GenericClass, metaclass=ABCMeta):
    children_instances = {}

    def __new__(cls, *args, **kwargs):
        if (cls.__name__ not in cls.children_instances):
            cls_obj = super(SolutionMethod, cls).__new__(cls)
            cls.children_instances[cls.__name__] = cls_obj
            HeuristicsObjects().add_object(cls_obj, SolutionMethod)

        return cls.children_instances[cls.__name__]


    def __init__(self, name):
        if (not hasattr(self, "name")):
            self.name = None

            # Acquired/created from input
            self.obj_func = None
            self.obj_func_name = None
            self.constraints = None
            self.constraints_names = None

            self.initialize_class_attributes()

    
    def route_is_feasible(self, route):
        for constraint in self.constraints:
            if (not constraint.route_is_feasible(route)):
                return False
        
        return True

    def solution_is_feasible(self, solution):
        for constraint in self.constraints:
            if (not constraint.solution_is_feasible(solution)):
                return False

        return True


    @abstractmethod
    def solve(self, solution, parameters):
        pass


    @abstractmethod
    def update_route_values(self, route, position, request):
        pass
    

    @staticmethod
    @abstractmethod
    def get_attr_relation_reader_heuristic():
        return {}
