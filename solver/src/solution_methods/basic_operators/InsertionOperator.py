
import copy
import time

from abc import ABCMeta, abstractmethod

from src import exceptions
from src import file_log
from src.GenericClass import GenericClass
from src.constraints.Constraint import Constraint

class InsertionOperator(GenericClass, metaclass=ABCMeta):

    instance = None

    def __new__(cls, *args, **kwargs):
        for subcls in GenericClass.get_all_subclasses(cls):
            if (subcls.instance is not None):
                return subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(InsertionOperator, cls).__new__(
                cls, *args, **kwargs
            )
        
        return cls.instance


    def __init__(self, insert_op_class_name=None):
        if (not hasattr(self, "name")):
            self.name = insert_op_class_name
            self.feasible_insertions_in_cache = set()
            self.feasible_insertions_cache = {}
            self.initialize_class_attributes()

    def check_feasibility(self, route, constraints):
        for constraint in constraints:
            if (not constraint.route_is_feasible(route)):
                return False
            
        return True

    def try_to_insert(self, route, position, request, obj_func, constraints):
        copy_route = route.copy()
        
        copy_route.insert(position, request)

        self.update_route_values(copy_route, position, request)
        additional_cost = obj_func.additional_route_cost_after_insertion(
            copy_route,
            position, 
            request
        )
        
        copy_route.route_cost += (
            additional_cost
        )

        feasible = self.check_feasibility(copy_route, constraints)
        if (not feasible):
            # for constraint in constraints:
            #     if (not constraint.route_is_feasible(copy_route)):
            return None
        
        return copy_route


    @abstractmethod
    def get_child_first_feasible_insertion(
        self,
        route, 
        request, 
        obj_func, 
        constraints
    ):
        pass


    def get_first_feasible_insertion(
        self,
        routes, 
        request, 
        obj_func, 
        constraints
    ):

        for route in routes:
            insertion = self.get_child_first_feasible_insertion(
                route,
                request,
                obj_func,
                constraints
            )
            if (not all(insertion)):
                continue
            
            return insertion

        return (None, None, None)



    @abstractmethod
    def get_child_class_route_feasible_insertions(
        self,
        route, 
        request, 
        obj_func, 
        constraints
    ): 
        """
        Return a list with a pair (position, new_route, insertion_cost) representing the inserting position and the route after insertio. If there is no feasible position, returns empty list.
        """
        pass



    def get_route_feasible_insertions(
        self, 
        route, 
        request, 
        obj_func, 
        constraints
    ):
        key = (request, route.get_id_value())
        if (key in self.feasible_insertions_in_cache):
            return self.feasible_insertions_cache[key]
        feasible_insertions = self.get_child_class_route_feasible_insertions(
            route, 
            request, 
            obj_func, 
            constraints
        )

        if (not route.empty()):
            self.feasible_insertions_in_cache.add(key)
            self.feasible_insertions_cache[key] = feasible_insertions

        return feasible_insertions



    def get_all_feasible_insertions_from_routes(
        self, 
        request, 
        routes, 
        obj_func,
        constraints
    ):

        feasible_insertions = []
        for route in routes:

            key = (request, route.get_id_value())

            feasible_insertion = []
            if (key not in self.feasible_insertions_in_cache):
                feasible_insertion = self.get_route_feasible_insertions(
                    route, 
                    request, 
                    obj_func, 
                    constraints
                )

            else:
                feasible_insertion = self.feasible_insertions_cache[key]

            feasible_insertions += feasible_insertion

        return feasible_insertions


    def get_all_feasible_insertions_from_solution(
        self, 
        request, 
        solution, 
        obj_func,
        constraints
    ):
        feasible_insertions = []
        for route in solution.routes():
            key = (request, route.get_id_value())

            feasible_insertion = []
            if (key not in self.feasible_insertions_in_cache):
                feasible_insertion = self.get_route_feasible_insertions(
                    route, 
                    request, 
                    obj_func, 
                    constraints
                )

            else:
                feasible_insertion = self.feasible_insertions_cache[key]

            feasible_insertions += feasible_insertion

        return feasible_insertions



    def get_best_insertion_in_route(
        self, 
        route, 
        request, 
        obj_func, 
        constraints
    ):
            
        feasible_positions = self.get_route_feasible_insertions(
            route, 
            request,
            obj_func,
            constraints
        )
        best_route = None
        best_insertion_position = None
        best_insert_cost = None

        for position, route, insert_cost in feasible_positions:
            if (obj_func.route_is_better(route, best_route)):
                best_route = route
                best_insertion_position = position
                best_insert_cost = insert_cost

        return (
            best_insertion_position,
            best_route,
            best_insert_cost
        )

    @abstractmethod
    def update_route_values(self, route, position, request, obj_func):
        pass


    @abstractmethod
    def update_solution_requests_costs_after_insertion(
        self, 
        solution, 
        route, 
        position, 
        request,
        obj_func
    ):
        pass


    @abstractmethod
    def get_attr_relation_reader(self):
        pass


    def insert_request_in_solution(
        self, 
        solution, 
        request, 
        request_pos,
        new_route,
        old_route_pos,
        obj_func
    ):

        solution.set_route(old_route_pos, new_route)
        solution.add_request(request)
        self.update_solution_requests_costs_after_insertion(
            solution, 
            new_route, 
            request_pos,
            request,
            obj_func
        )

        return solution

    def remove_route_from_feasible_insertions_cache(self, request, route):
        key = (request, route.get_id_value())
        self.feasible_insertions_in_cache.discard(key)

    
    def clean_feasible_insertions_cache(self):
        self.feasible_insertions_in_cache = set()
        self.feasible_insertions_cache = {}

    def clean_feasible_insertions_cache_with_exception(self, routes):
        keys_in_cache = copy.deepcopy(self.feasible_insertions_in_cache)

        cache_keys_exceptions = set()
        cache_exceptions = {}

        for route in routes:
            route_id_value = route.get_id_value()
            
            for key in self.feasible_insertions_in_cache:
                request, id_value = key

                if (route_id_value == id_value):
                    cache_keys_exceptions.add(key)
                    cache_exceptions[key] = self.feasible_insertions_cache[key]
                
        self.feasible_insertions_in_cache = cache_keys_exceptions
        self.feasible_insertions_cache = cache_exceptions



    def get_route_id_value_before_inserted(
        self, 
        route, 
        request_inserted
    ):
        try:
            len(request_inserted)
        except:
            request_inserted = (request_inserted)
        old_route_identifying = route.get_id_value_without_request(
            request_inserted
        )

        return old_route_identifying
    
    
    @staticmethod
    def clear():
        for subcls in InsertionOperator.__subclasses__():
            subcls.instance = None
        InsertionOperator.instance = None