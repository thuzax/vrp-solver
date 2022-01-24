import copy
from os import stat
from src.route_classes import Route

from abc import ABC, ABCMeta, abstractmethod
import typing

from src import exceptions
from src.GenericClass import GenericClass


class RouteClass(GenericClass, metaclass=ABCMeta):

    def __init__(self, route_class_name=None):
        if (not hasattr(self, "name")):
            self.name = route_class_name
            self.vertices_order = []
            self.requests_set = set()
            self.route_cost = 0
            self.id_value = ()
            self.initialize_class_attributes()


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
        if (self.id_value is None):
            return False
        
        if (route.id_value is None):
            return False
        
        if (self.id_value != route.id_value):
            return False
        
        return True


    def has_same_requests(self, route):
        if (self.requests_set == route.requests_set):
            return True
        
        return False


    def calculate_route_id_value(self):
        self.id_value = tuple(self.vertices_order)


    def get_id_value(self):
        return self.id_value


    def __contains__(self, key):
        if (key in self.requests_set):
            return True
        
        return False


    def __str__(self):
        return str(self.vertices_order)



    @abstractmethod
    def insert_in_route(self, insert_position, request, params):
        pass
    
    def insert(self, insert_position, request, params):
        self.insert_in_route(insert_position, request, params)
        self.calculate_route_id_value()


    @abstractmethod
    def index(self, request):
        pass


    def remove(self, request):
        position = self.index(request)
        self.pop(position)

    
    @abstractmethod
    def pop_from_route(self, position):
        pass


    def pop(self, position):
        request = self.pop_from_route(position)
        self.calculate_route_id_value()
        return request


    @abstractmethod
    def cost(self):
        return self.route_cost

    
    @abstractmethod
    def copy_route_to(self, route_copy):
        pass

    def copy(self):
        route_copy = Route()
        
        route_copy.vertices_order = copy.deepcopy(self.vertices_order)
        route_copy.requests_set = copy.deepcopy(self.requests_set)
        route_copy.route_cost = copy.deepcopy(self.route_cost)
        route_copy.id_value = copy.copy(self.id_value)
        
        self.copy_route_to(route_copy)

        return route_copy


    @staticmethod
    @abstractmethod
    def get_attr_relation_reader_route():
        pass

    
    @staticmethod
    def clear():
        pass