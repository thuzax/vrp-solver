from abc import ABCMeta, abstractmethod
from src.GenericClass import GenericClass

class RemovalOperator(GenericClass, metaclass=ABCMeta):

    instance = None

    def __new__(cls, *args, **kwargs):
        for subcls in cls.__subclasses__():
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



    @abstractmethod
    def try_to_remove(self, route, request, obj_func, constraints):
        copy_route = route.copy()

        position = copy_route.index(request)
        copy_route.pop(position)

        self.update_route_values(copy_route, position, request)

        copy_route.route_cost += (
            obj_func.route_reduced_route_cost_before_removal(
                route,
                position, 
                request
            )
        )

        for constraint in constraints:
            if (self.route_is_feasible(copy_route)):
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
