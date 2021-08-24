
from abc import ABCMeta, abstractmethod

from src import exceptions
from src.heuristics.HeuristicsObjects import HeuristicsObjects
from src.GenericClass import GenericClass


class Heuristic(GenericClass, metaclass=ABCMeta):
    children_instances = {}

    def __new__(cls, *args, **kwargs):
        if (cls.__name__ not in cls.children_instances):
            cls_obj = super(Heuristic, cls).__new__(cls)
            cls.children_instances[cls.__name__] = cls_obj
            HeuristicsObjects().add_object(cls_obj)

        return cls.children_instances[cls.__name__]


    def __init__(self, name):
        if (not hasattr(self, "name")):
            self.name = None

            # Acquired/created from input
            self.obj_func = None
            self.obj_func_name = None
            self.constraints = None
            self.constraints_names = None


    @abstractmethod
    def solve(self, parameters):
        pass

    @staticmethod
    @abstractmethod
    def get_attr_relation_reader_heuristic():
        return {}
