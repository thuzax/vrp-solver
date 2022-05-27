from abc import ABCMeta, abstractmethod
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
from src.GenericClass import GenericClass

class RemovalOperator(GenericClass, metaclass=ABCMeta):

    instance = None

    def __new__(cls, *args, **kwargs):
        for subcls in GenericClass.get_all_subclasses(cls):
            if (subcls.instance is not None):
                return subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(RemovalOperator, cls).__new__(
                cls, *args, **kwargs
            )
        return cls.instance

    def __init__(self, insert_op_class_name=None):
        if (not hasattr(self, "name")):
            self.name = insert_op_class_name
            self.initialize_class_attributes()



    def check_feasibility(self, route, constraints):
        for constraint in constraints:
            if (not constraint.route_is_feasible(route)):
                return False
            
        return True


    @abstractmethod
    def try_to_remove(self, route, request, obj_func, constraints):
        copy_route = route.copy()
        position = copy_route.index(request)
        request = copy_route.pop(position)

        self.update_route_values(copy_route, position, request)

        copy_route.route_cost += (
            obj_func.route_reduced_route_cost_before_removal(
                route,
                position, 
                request
            )
        )

        feasible = self.check_feasibility(copy_route, constraints)
        if (not feasible):
            return None
        
        return copy_route

    @abstractmethod
    def update_solution_requests_costs_after_removal(
        self, 
        solution, 
        route, 
        position, 
        request,
        obj_func
    ):
        pass

    @abstractmethod
    def get_attr_relation_reader_remov_op(self):
        return {}


    def remove_request_from_solution(
        self, 
        solution, 
        request, 
        request_pos,
        new_route,
        old_route_pos,
        obj_func
    ):
        solution.remove_request(request)
        solution.set_route(old_route_pos, new_route)
        self.update_solution_requests_costs_after_removal(
            solution, 
            new_route,
            request_pos,
            request,
            obj_func
        )

        return solution
        
    
    @staticmethod
    def clear():
        for subcls in RemovalOperator.__subclasses__():
            subcls.instance = None
        RemovalOperator.instance = None