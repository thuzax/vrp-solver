import numpy

from abc import ABC, ABCMeta, abstractmethod
import typing

from src import exceptions, route_classes


class RouteSubClass:
    instance = None
    route_subclass = None
    route_subclass_params = None

    def __new__(cls, *args, **kwargs):
        if (len(cls.__subclasses__())):
            raise exceptions.ClassCannotBeInherited("RouteSubClass")

        if (cls.instance is None):
            cls.instance = super(RouteSubClass, cls).__new__(cls)

        return cls.instance


    def __init__(self, subclass=None):
        if (subclass is not None):
            self.route_subclass = subclass


create_super = False
class Route(metaclass=ABCMeta):

    name = None
    child_created = False


    def __new__(cls, *args, **kwargs):
        global create_super
        
        if (create_super):
            cls = super(Route, cls).__new__(cls, *args, **kwargs)
            create_super = False
            return cls
        
        create_super = True
        cls = RouteSubClass().route_subclass()
        cls.child_created = True
        return cls


    def __init__(self, route_class_name=None):
        if (self.child_created):
            self.name = route_class_name
            self.vertices_order = []
            self.vertices_set = set()

            route_input_params = RouteSubClass.route_subclass_params
            for param_name, param_value in route_input_params.items():
                self.set_attribute(param_name, param_value)


    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                self.__class__.__name__, 
                name
            )
            
        self.__setattr__(name, value)


    def __contains__(self, key):
        if (key in self.vertices_set):
            return True
        return False


    def __str__(self):
        return str(self.vertices_order)


    @abstractmethod
    def insert(self, vertex):
        pass

    @abstractmethod
    def remove(self, vertex):
        pass

    @staticmethod
    def get_solver_route_attribute_relation():
        route_subclass = RouteSubClass().route_subclass
        sol_rout_attr = route_subclass.get_attribute_relation_solver_route()
        return sol_rout_attr

    @staticmethod
    @abstractmethod
    def get_attribute_relation_solver_route():
        pass

    @staticmethod
    def update_route_class_params(params):
        RouteSubClass.route_subclass_params = params
