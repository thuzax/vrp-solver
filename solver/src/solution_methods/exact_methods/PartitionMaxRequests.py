from pdb import line_prefix
import time
from mip import *

from src import file_log, route_classes

from src.solution_classes import Solution
from src.solution_methods.exact_methods.SBSolver import SBSolver

class PartitionMaxRequests(SBSolver):
    
    def __init__(self):
        if (not hasattr(self, "name")):
            super().__init__("PartitionMaxRequests")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.max_routes_cost_increment = None
        
        self.fleet_size = None
        self.fixed_routes_dict =None



    def make_model_obj_func(self, model, parameters):
        variables = model.vars
        requests = parameters["requests_set"]
        
        x = {
            request : model.var_by_name("x_"+str(request))
            for request in requests
        }

        model.objective = xsum(
            -x[request]
            for request in requests
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

        requests = parameters["requests_set"]
        x = [
            model.add_var(
                var_type=BINARY, 
                name="x_"+str(request)
            )
            for request in requests
        ]
        return model.vars


    def initialize_model(self, model, solution, parameters):
        routes_pool = parameters["routes_pool"]
        
        initial_routes_pos = set()
        for i, route_1 in enumerate(routes_pool):
            for route_2 in solution.routes():
                if (route_1.is_equal(route_2)):
                    initial_routes_pos.add(i)

        y_start = [
            (
                model.var_by_name("y_"+str(i)), 
                1 if i in initial_routes_pos else 0
            ) 
            for i in range(len(routes_pool))
        ]


        requests = parameters["requests_set"]
        x_start = [
            (
                model.var_by_name("x_"+str(request)),
                1 if request in solution else 0
            )
            for request in requests
        ]

        model.start = y_start + x_start



    def make_constraints(self, model, solution, request_in_route, parameters):
        routes_pool = parameters["routes_pool"]
        y = [
            model.var_by_name("y_"+str(i))
            for i in range(len(routes_pool))
        ]

        # Request cannot repeat
        for request in request_in_route:
            n_req_in_routes_sum = xsum(
                request_in_route[request][i] * y[i] 
                for i in range(len(routes_pool))
            )
            
            model.add_constr(
                lin_expr=(n_req_in_routes_sum <= 1), 
                name="one_attendance_"+str(request)
            )

            req_var = model.var_by_name("x_"+str(request))
            model.add_constr(
                lin_expr=(req_var == n_req_in_routes_sum),
                name="x_"+str(request)+"_was_chosen"
            )
        
        # Limited Fleet
        n_routes_sum = xsum(
            y[i]
            for i in range(len(routes_pool))
        )

        model.add_constr(
            lin_expr=(n_routes_sum <= self.fleet_size),
            name="limited_fleet"
        )

        # Routes Cost cannot be worser than a maximum percentage
        max_cost = (
            (1 + self.max_routes_cost_increment) 
            * solution.routes_cost()
        )

        sol_cost = xsum(
            y[i] * routes_pool[i].cost()
            for i in range(len(routes_pool))
        )

        model.add_constr(
            lin_expr=(sol_cost <= max_cost),
            name="max_cost"
        )

        # Fixed requests must be present
        for route_dict in self.fixed_routes_dict:
            for request in route_dict["requests"]:
                req_var = model.var_by_name("x_"+str(request))
                model.add_constr(
                    lin_expr=(req_var == 1),
                    name="x_"+str(request)+"_is_fixed"
                )
            
        # for cons in model.constrs:
        #     print(cons)


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


    def get_attr_relation_reader_heuristic(self):
        return {
            "fleet_size" : "fleet_size",
            "fixed_routes_dict" : "fixed_routes_dict"
        }