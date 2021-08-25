from abc import ABC, ABCMeta, abstractmethod
from src.objects_managers.ObjFunctionsObjects import ObjFunctionsObjects

from src import exceptions
from src.GenericClass import GenericClass


class ObjFunction(GenericClass, metaclass=ABCMeta):
    children_instances = {}


    def __new__(cls, *args, **kwargs):
        if (cls.__name__ not in cls.children_instances):
            cls_obj = super(ObjFunction, cls).__new__(cls)
            cls.children_instances[cls.__name__] = cls_obj
            ObjFunctionsObjects().add_object(cls_obj, ObjFunction)
        
        return cls.children_instances[cls.__name__]


    def __init__(self, name):
        if (not hasattr(self, "name")):
            self.name = name
            self.initialize_class_attributes()


    @abstractmethod
    def get_route_cost(self, route_order):
        pass


    @abstractmethod
    def get_solution_cost(self, solution):
        pass


    @abstractmethod
    def request_inserted_additional_route_cost(self, route, positions, request):
        """Calculate the increasing cost of route. It is considered that the 'request' inserted in 'positions' were the last insertion on the route and that the cost were updated.\n
        -Parameters:\n
        route -> Route() object;\n
        positions -> position(s) of insertion;\n
        request -> request inserted"""
        pass


    @staticmethod
    @abstractmethod
    def route_is_better(route_1, route_2):
        pass

    @staticmethod
    @abstractmethod
    def get_attr_relation_reader_func():
        pass

    