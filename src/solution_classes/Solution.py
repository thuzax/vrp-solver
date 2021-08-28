import copy
import numpy

from abc import ABC, ABCMeta, abstractmethod
import typing

from src import exceptions
from src.GenericClass import GenericClass


class Solution(GenericClass):

    instance = None


    def __new__(cls, *args, **kwargs):
        if (cls.instance is None):
            cls.instance = super(Solution, cls).__new__(cls)

        return cls.instance


    def __init__(self, solution_class_name=None):
        self.name = solution_class_name
        self.initialize_class_attributes()


    def initialize_class_attributes(self):

        self.routes = []

        self.requests_set = set()
        self.requests_cost_dict = {}
        
        self.total_routes_cost = 0
        self.solution_cost = 0
        


    def add_route(self, route):
        self.routes.append(route)
        self.total_routes_cost += route.cost()
    
    
    def add_request(self, request):
        self.requests_set.add(request)
        self.requests_cost_dict[request] = None

    
    def remove_request(self, request):        
        self.requests_set.remove(request)
        self.requests_cost_dict.pop(request)

    
    def pop_route(self, route_position):
        route = self.routes.pop(route_position)
        
        for request in route.get_requests_set():
            self.remove_request(request)

        self.solution_cost -= 1
        return route


    def set_route(self, route_id, new_route):
        self.total_routes_cost -= self.routes[route_id].cost()
        self.total_routes_cost += new_route.cost()
        self.routes[route_id] = new_route


    def set_request_cost(self, request, cost):
        self.requests_cost_dict[request] = cost


    def set_objective_value(self, new_value):
        self.solution_cost = new_value



    def __str__(self):
        text = ""
        text += "******************************************************" + "\n"
        text += "************************ROUTES************************" + "\n"
        for route in self.routes:
            text += str(route) + "\n"
        text += "******************************************************" + "\n"
        text += "***********************REQUESTS***********************" + "\n"
        text += "SET: " + str(self.requests_set) + "\n"
        text += "COST: " + str(self.requests_cost_dict) + "\n"
        text += "******************************************************" + "\n"
        text += "ROUTES COST: " + str(self.total_routes_cost) + "\n"
        text += "SOLUTION COST: " + str(self.solution_cost) + "\n"
        text += "******************************************************" + "\n"
        text += "******************************************************" + "\n"
        return text


    def copy(self):
        copy_solution = Solution()
        copy_solution.requests_set = copy.deepcopy(self.requests_set)
        copy_solution.requests_cost_dict = copy.deepcopy(self.requests_cost_dict)
        copy_solution.routes = [route.copy() for route in self.routes]
        copy_solution.total_routes_cost = self.total_routes_cost

        return copy_solution


    def routes_cost(self):
        return self.total_routes_cost


    def cost(self):
        return self.solution_cost


    def requests(self):
        return self.requests_set


    def requests_costs(self):
        return self.requests_cost_dict


    def get_reader_solut_attr_relation(self):
        return {
        }
