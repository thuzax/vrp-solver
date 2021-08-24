from abc import ABCMeta, abstractmethod

from src.GenericClass import GenericClass
from src.constraints.ConstraintObjects import ConstraintsObjects

class Constraint(GenericClass, metaclass=ABCMeta):
    
    children_instances = {}

    def __new__(cls, *args, **kwargs):
        if (cls.__name__ not in cls.children_instances):
            cls_obj = super(Constraint, cls).__new__(cls)
            cls.children_instances[cls.__name__] = cls_obj
            ConstraintsObjects().add_object(cls_obj)

        return cls.children_instances[cls.__name__]

    def __init__(self, name):
        if (not hasattr(self, "name")):
            self.name = name


    @abstractmethod
    def route_is_feasible(self, route):
        pass
    

    def solution_is_feasible(self, solution):
        for route in solution:
            if (not self.route_is_feasible(route)):
                return False

        return True


    @staticmethod
    @abstractmethod
    def get_attr_relation_solver_constr():
        pass