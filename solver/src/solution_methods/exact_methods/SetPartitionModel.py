import time
from mip import *

from src import file_log, route_classes

from src.solution_classes import Solution
from src.solution_methods.exact_methods.SBSolver import SBSolver

class SetPartitionModel(SBSolver):
    
    def __init__(self):
        if (not hasattr(self, "name")):
            super().__init__("SetPartitionModel")


    def make_model_obj_func(self, model, parameters):
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
        


    def make_constraints(self, model, solution, request_in_route, parameters):
        y = model.vars
        routes_pool = parameters["routes_pool"]
        for request in request_in_route:
            n_routes_sum = xsum(
                request_in_route[request][i] * y[i] 
                for i in range(len(routes_pool))
            )
            model.add_constr(
                lin_expr=(n_routes_sum == 1), 
                name="one_attendance_"+str(request)
            )
        

    def construct_solution_from_model(self, model, parameters):
        y = model.vars
        routes_pool = parameters["routes_pool"]
        new_soltuion = Solution()
        for i in range(len(routes_pool)):
            if (y[i].x):
                new_soltuion.add_route(routes_pool[i])
                for request in routes_pool[i].requests():
                    new_soltuion.add_request(request)
                    request_cost = self.obj_func.get_request_cost_in_route(
                        routes_pool[i],
                        routes_pool[i].index(request),
                        request
                    )
                    new_soltuion.set_request_cost(request, request_cost)
                
                new_soltuion.set_objective_value(
                    self.obj_func.get_solution_cost(new_soltuion)
                )
        return new_soltuion
