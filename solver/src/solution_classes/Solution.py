import copy
import numpy

from abc import ABC, ABCMeta, abstractmethod
import typing

from src import exceptions
from src.GenericClass import GenericClass
from src.route_classes.RouteClass import RouteClass


class Solution(GenericClass):

    def __init__(self, solution_class_name=None):
        self.name = solution_class_name
        self.initialize_class_attributes()


    def initialize_class_attributes(self):
        self.routes_list = []

        self.requests_set = set()
        self.requests_cost_dict = {}
        
        self.total_routes_cost = 0
        self.solution_cost = 0
        

    def add_route(self, route):
        self.routes_list.append(route)
        self.total_routes_cost += route.cost()
    
    
    def add_request(self, request):
        self.requests_set.add(request)
        self.requests_cost_dict[request] = None

    
    def remove_request(self, request):
        self.requests_set.remove(request)
        self.requests_cost_dict.pop(request)

    
    def pop_route(self, route_position):
        route = self.routes_list.pop(route_position)
        
        for request in route.requests():
            self.remove_request(request)

        self.total_routes_cost -= route.cost()
        
        return route


    def remove_route(self, route_pos):
        self.pop_route(route_pos)


    def set_route(self, route_pos, new_route):
        self.total_routes_cost -= self.routes_list[route_pos].cost()
        self.total_routes_cost += new_route.cost()
        self.routes_list[route_pos] = new_route


    def set_request_cost(self, request, cost):
        self.requests_cost_dict[request] = cost


    def set_objective_value(self, new_value):
        self.solution_cost = new_value


    def set_routes_cost(self, new_value):
        self.total_routes_cost = new_value


    def find_route_position_by_identifying_value(self, route_id_value):
        for i in range(len(self.routes_list)):
            route_i_id_value = self.routes_list[i].get_id_value()
            if (route_i_id_value == route_id_value):
                return i
        return None


    def __str__(self):
        text = ""
        text += "******************************************************" + "\n"
        text += "************************ROUTES************************" + "\n"
        for route in self.routes_list:
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
        copy_solution.requests_cost_dict = copy.deepcopy(
            self.requests_cost_dict
        )

        copy_solution.routes_list = [route.copy() for route in self.routes_list]

        copy_solution.total_routes_cost = self.total_routes_cost

        copy_solution.solution_cost = self.solution_cost

        return copy_solution


    def routes_cost(self):
        return self.total_routes_cost


    def cost(self):
        return self.solution_cost


    def requests(self):
        return self.requests_set


    def routes(self):
        return self.routes_list


    def requests_costs(self):
        return self.requests_cost_dict


    def get_request_route(self, request):
        for route_pos, route in enumerate(self.routes_list):
            if request in route:
                return (route_pos, route)
            
        return None


    def number_of_routes(self):
        return len(self.routes_list)

    def number_of_empty_routes(self):
        empty_m = 0
        for route in self.routes_list:
            if (route.empty()):
                empty_m += 1
        
        return empty_m

    def number_of_non_empty_routes(self):
        return (
            self.number_of_routes() 
            - self.number_of_empty_routes()
        )


    def number_of_requests(self):
        return len(self.requests_set)


    def get_costs_output_text(self):
        text = ""
        text += "obj_value: " + str(self.cost()) + "; "
        text += "obj_routes: " + str(self.routes_cost())
        return text


    def get_routes_output_text(self):
        text = ""
        for i, route in enumerate(self.routes_list):
            text += "Route " + str(i+1) + " : "
            for vertex_id in route.requests_order():
                text += str(vertex_id) + " "

            text += "\n"
        return text

    def get_dict(self):
        sol_dict = {}
        sol_dict["routes"] = {}
        sol_dict["costs"] = {}
        for i, route in enumerate(self.routes_list):
            sol_dict["routes"][i] = [
                int(vertex_id) 
                for vertex_id in route.requests_order()
            ]
            sol_dict["costs"][i] = float(route.cost())

        sol_dict["solution_cost"] = float(self.cost())
        sol_dict["solution_routes_cost"] = float(self.routes_cost())
        return sol_dict


    def get_reader_solut_attr_relation(self):
        return {
        }
    
    
    def __contains__(self, item):
        if (isinstance(item, RouteClass)):
            item_id = item.get_id_value()
            route_pos_in_sol = (
                self.find_route_position_by_identifying_value(item_id)
            )
            if (route_pos_in_sol is not None):
                return True
        
        if (isinstance(item, tuple) and len(item) == 2):
            if (item in self.requests_set):
                return True
        
        return False
            
            


    @staticmethod
    def clear():
        pass
