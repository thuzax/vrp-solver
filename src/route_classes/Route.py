import numpy

from abc import ABC, ABCMeta, abstractmethod
import typing

from src import exceptions
from src.GenericClass import GenericClass


class RouteSubClass:
    instance = None
    route_subclass = None
    route_subclass_params = None
    route_id_counter = 0

    def __new__(cls, *args, **kwargs):
        if (len(cls.__subclasses__())):
            raise exceptions.ClassCannotBeInherited("RouteSubClass")

        if (cls.instance is None):
            cls.instance = super(RouteSubClass, cls).__new__(cls)

        return cls.instance


    def __init__(self, subclass=None):
        if (subclass is not None):
            self.route_subclass = subclass


    def get_next_route_id(self):
        route_id = self.route_id_counter
        self.route_id_counter += 1
        return route_id



create_super = False
class Route(GenericClass, metaclass=ABCMeta):

    child_created = False

    def __new__(cls, *args, **kwargs):
        global create_super
        
        if (create_super):
            cls = super(Route, cls).__new__(cls, *args, **kwargs)
            create_super = False
            return cls
        
        create_super = True
        cls = RouteSubClass().route_subclass()
        cls.route_id = RouteSubClass().get_next_route_id()
        cls.child_created = True
        return cls


    def __init__(self, route_class_name=None):
        if (not hasattr(self, "name")):
            self.name = route_class_name
            self.vertices_order = []
            self.requests_set = set()
            self.requests = []
            self.route_id = 0
            self.route_cost = 0
            self.initialize_class_attributes()
            self.set_input_params()


    def set_input_params(self):
        route_input_params = RouteSubClass.route_subclass_params
        if (route_input_params is None):
            return
        for param_name, param_value in route_input_params.items():
            self.set_attribute(param_name, param_value)
            

    def get_previous_vertex_of_position(self, position):
        if (position <= 0):
            return None
        
        if (position > self.size()):
            return None

        return self.vertices_order[position-1]


    def get_next_vertex_of_position(self, position):
        if (position >= self.size()-1):
            return None
        
        if (position < 0):
            return None

        return self.vertices_order[position+1]

    
    def get_order(self):
        return self.vertices_order

        
    def get_requests_set(self):
        return self.requests_set

    @abstractmethod
    def get_request_by_position(self, position):
        pass


    def empty(self):
        if (self.size() == 0):
            return True

        return False


    def size(self):
        return len(self.vertices_order)


    def __contains__(self, key):
        if (key in self.requests_set):
            return True
        return False


    def __str__(self):
        return str(self.vertices_order)



    @abstractmethod
    def insert(self, insert_position, request, obj_func):
        pass


    @abstractmethod
    def index(self, request):
        pass


    @abstractmethod
    def remove(self, request):
        pass


    @abstractmethod
    def pop(self, request):
        pass


    @abstractmethod
    def cost(self):
        return self.route_cost

    
    @abstractmethod
    def copy(self):
        pass


    @abstractmethod
    def get_id(self):
        return self.route_id


    @staticmethod
    @abstractmethod
    def get_attr_relation_reader_route():
        pass


    @staticmethod
    def get_reader_route_attr_relation():
        route_subclass = RouteSubClass().route_subclass
        reader_rout_attr = route_subclass.get_attr_relation_reader_route()
        return reader_rout_attr


    @staticmethod
    def update_route_class_params(params):
        RouteSubClass.route_subclass_params = params
