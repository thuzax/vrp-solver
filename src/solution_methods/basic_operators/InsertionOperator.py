
from abc import ABCMeta, abstractmethod

from src import exceptions
from src.GenericClass import GenericClass


class InsertionOperator(GenericClass, metaclass=ABCMeta):

    instance = None

    def __new__(cls, *args, **kwargs):
        for subcls in cls.__subclasses__():
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
            self.initialize_class_attributes()


    @abstractmethod
    def try_to_insert(self, route, position, request, obj_func, constraints):
        copy_route = route.copy()
        copy_route.insert(position, request)

        self.update_route_values(copy_route, position, request)
        copy_route.route_cost += (
            obj_func.route_additional_route_cost_after_insertion(
                copy_route,
                position, 
                request
            )
        )

        for constraint in constraints:
            if (not constraint.route_is_feasible(copy_route)):
                return None
        return copy_route


    @abstractmethod
    def get_route_feasible_insertions(
        self, 
        route, 
        request, 
        obj_func, 
        constraints
    ):
        """
        Return a list with a pair (position, new_route) representing the inserting position and the route after insertio. If there is no feasible position, returns empty list.
        """
        pass


    def get_all_feasible_insertions_from_routes(
        self, 
        request, 
        routes, 
        obj_func,
        constraints
    ):
        feasible_insertions = []
        for route in routes:
            feasible_insertions.append(
                self.get_route_feasible_insertions(
                    route, 
                    request, 
                    obj_func, 
                    constraints
                )
            )

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

        for position, route in feasible_positions:
            if (obj_func.route_is_better(route, best_route)):
                best_route = route
                best_insertion_position = position

        return (
            best_insertion_position,
            best_route
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
    def get_attr_relation_reader_insert_op(self):
        pass
