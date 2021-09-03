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
    def get_route_cost(self, route):
        pass


    def get_routes_sum_cost(self, routes):
        cost = 0
        for route in routes:
            cost += self.get_route_cost(route)
        return cost


    @abstractmethod
    def get_solution_cost(self, solution):
        pass


    @abstractmethod
    def route_additional_route_cost_after_insertion(
        self, 
        route, 
        position, 
        request
    ):
        """Calculate the increasing cost of route. It is considered that the 'request' inserted in 'positions' were the last insertion on the route and that the cost were updated.\n
        -Parameters:\n
        route -> Route() object;\n
        positions -> tuple of positions where request was inserted (pickup_pos, delivery_pos);\n
        request -> inserted request;"""
        pass

    @abstractmethod
    def route_reduced_route_cost_before_removal(self, route, position, request):
        """Calculate the deacresing cost of route. It is considered that the 'request' was not removed yet and its position in route is 'position'.\n
        -Parameters:\n
        route -> Route() object;\n
        position -> position(s) of the removed;\n
        request -> request inserted"""
        pass

    
    @abstractmethod
    def get_request_cost_in_route(self, route, position, request):
        """The request cost is how much the route cost increase when the request is in route. Inputs: a route, the position where request is inserted, the request.
        """
        pass


    @staticmethod
    def route_is_better(route_1, route_2):
        if (route_1 is None):
            return False
        
        if (route_2 is None):
            return True

        if (route_1.cost() > route_2.cost()):
            return False
        
        return True


    @staticmethod
    def solution_is_better(s_1, s_2):
        if (s_1 is None):
            return False
        
        if (s_2 is None):
            return True

        if (s_1.cost() > s_2.cost()):
            return False

        if (
            (s_1.cost() == s_2.cost()) 
            and (s_1.routes_cost() >= s_2.routes_cost())
        ):
            return False
        return True


    @staticmethod
    def solution_obj_better_than_value(solution, obj_value):
        if (solution is None):
            return False
        
        if (obj_value is None):
            return True
        
        if (solution.cost() > obj_value[0]):
            return False
        
        if (
            (solution.cost() == obj_value[0]) 
            and (solution.routes_cost() > obj_value[1])
        ):
            return False

        return True