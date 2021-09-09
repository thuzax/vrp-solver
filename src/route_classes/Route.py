import copy
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
            self.route_id = 0
            self.route_cost = 0
            self.identifying_value = None
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

    
    def requests_order(self):
        return self.vertices_order

        
    def requests(self):
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

    def number_of_requests(self):
        return len(self.requests_set)


    def is_equal(self, route):
        if (self.identifying_value is None):
            return False
        
        if (route.identifying_value is None):
            return False
        
        if (self.identifying_value != route.identifying_value):
            return False
        
        return True

    def change_id(self):
        self.route_id = RouteSubClass().get_next_route_id()
        return self

    def calculate_route_identifying_value(self):
        self.identifying_value = tuple(self.vertices_order)
        # string_order = [str(v) for v in self.vertices_order]
        # self.identifying_value = ".".join(string_order)


    def get_identifying_value(self):
        return self.identifying_value


    def __contains__(self, key):
        if (key in self.requests_set):
            return True
        
        return False


    def __str__(self):
        return str(self.vertices_order)



    @abstractmethod
    def insert_in_route(self, insert_position, request):
        pass
    
    def insert(self, insert_position, request):
        self.insert_in_route(insert_position, request)
        self.calculate_route_identifying_value()


    @abstractmethod
    def index(self, request):
        pass


    @abstractmethod
    def remove(self, request):
        pass

    
    @abstractmethod
    def pop_from_route(self, position):
        pass


    def pop(self, position):
        request = self.pop_from_route(position)
        self.calculate_route_identifying_value()
        return request


    @abstractmethod
    def cost(self):
        return self.route_cost

    
    @abstractmethod
    def copy_route(self):
        pass

    def copy(self):
        copy_route = self.copy_route()

        copy_route.route_id = self.route_id
        copy_route.vertices_order = copy.deepcopy(self.vertices_order)
        copy_route.requests_set = copy.deepcopy(self.requests_set)
        
        copy_route.route_cost = copy.deepcopy(self.route_cost)

        copy_route.identifying_value = copy.copy(self.identifying_value)

        return copy_route


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
