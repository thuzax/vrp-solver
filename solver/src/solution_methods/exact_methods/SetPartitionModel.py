import time
from mip import *

from src import file_log, route_classes

from src.solution_classes import Solution
from src.solution_methods.exact_methods.SBSolver import SBSolver

class SetPartitionModel(SBSolver):
    
    def __init__(self):
        if (not hasattr(self, "name")):
            super().__init__("SetPartitionModel")


    def make_model_obj_func(self, model, solution, parameters):
        y = model.vars
        routes_pool = parameters["routes_pool"]
        model.objective = xsum(
            routes_pool[i].cost() * y[i]
            for i in range(len(routes_pool))
        )
    

    def create_variables(self, model, parameters):
        routes_pool = parameters["routes_pool"]
        y = [
            model.add_var(
                var_type=BINARY, 
                name="y_"+str(i)
            )
            for i in range(len(routes_pool))
        ]
        return y


    def initialize_model(self, model, solution, parameters):
        routes_pool = parameters["routes_pool"]

        initial_routes_pos = set()
        for i, route in enumerate(routes_pool):
            if (route in solution):
                initial_routes_pos.add(i)

        model.start = [
            (
                model.var_by_name("y_"+str(i)), 
                1 if i in initial_routes_pos else 0
            ) 
            for i in range(len(routes_pool))
        ]
        


    def make_constraints(
        self, 
        model, 
        solution, 
        routes_with_request, 
        parameters
    ):
        y = model.vars
        routes_pool = parameters["routes_pool"]
        for request in routes_with_request:
            n_req_in_routes_sum = xsum(
                y[i] 
                for i in routes_with_request[request]
            )
            
            model.add_constr(
                lin_expr=(n_req_in_routes_sum == 1), 
                name="one_attendance_"+str(request)
            )

    def construct_solution_from_model(self, model, parameters):
        return super().construct_solution_from_model(model, parameters)