import time
from mip import *
from src.route_classes import Route

from src.solution_classes import Solution
from src.solution_methods.exact_methods.SBSolver import SBSolver

class PartitionMaxRequests(SBSolver):
    
    def __init__(self):
        if (not hasattr(self, "name")):
            super().__init__("PartitionMaxRequests")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.max_routes_cost_increment = None
        
        self.fleet = None
        self.fixed_routes_dict = None

        self.cost_reduction_factor = None



    def make_model_obj_func(self, model, solution, parameters):
        requests = parameters["requests_set"]
        routes_pool = parameters["routes_pool"]

        x = {
            request : model.var_by_name("x_"+str(request))
            for request in requests
        }

        y = [
            model.var_by_name("y_"+str(i))
            for i in range(len(routes_pool))
        ]

        # Make a set with non-fixed requests
        fixed_requests = set()
        for route_dict in self.fixed_routes_dict:
            for request in route_dict["requests"]:
                fixed_requests.add(request)

        non_fixed_requests = requests - fixed_requests

        # obj function uses only non-fixed_requests
        
        sol_cost = xsum(
            y[i] * routes_pool[i].cost()
            for i in range(len(routes_pool))
        )

        # Consider solution cost
        model.objective = (
            - xsum(
                x[request]
                for request in non_fixed_requests
            )
            +
            self.cost_reduction_factor * (sol_cost/solution.routes_cost())
        )
    

    def create_variables(self, model, parameters):
        routes_pool = parameters["routes_pool"]
        y = [
            model.add_var(
                var_type=INTEGER,
                ub = 1,
                lb = 0, 
                name="y_"+str(i)
            )
            for i in range(len(routes_pool))
        ]

        requests = parameters["requests_set"]
        x = [
            model.add_var(
                var_type=INTEGER, 
                ub = 1,
                lb = 0,
                name="x_"+str(request)
            )
            for request in requests
        ]

        return model.vars


    def get_variables_start_value(self, model, solution, parameters):
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
        return (y_start + x_start)


    def initialize_model(self, model, solution, parameters):

        model.start = self.get_variables_start_value(
            model, 
            solution, 
            parameters
        )


    def request_chosen(
        self, 
        model, 
        routes_pool, 
        routes_with_request 
    ):
        y = [
            model.var_by_name("y_"+str(i))
            for i in range(len(routes_pool))
        ]

        for request in routes_with_request:
            n_req_in_routes_sum = xsum(
                y[i] 
                for i in routes_with_request[request]
            )

            req_var = model.var_by_name("x_"+str(request))
            model.add_constr(
                lin_expr=(req_var == n_req_in_routes_sum),
                name="x_"+str(request)+"_was_chosen"
            )


    def limited_fleet_constr(self, model, routes_pool):
        y = [
            model.var_by_name("y_"+str(i))
            for i in range(len(routes_pool))
        ]

        n_routes_sum = xsum(
            y[i]
            for i in range(len(routes_pool))
        )

        model.add_constr(
            lin_expr=(n_routes_sum <= self.fleet),
            name="limited_fleet"
        )


    def routes_max_cost_constr(self, model, solution, routes_pool):
        y = [
            model.var_by_name("y_"+str(i))
            for i in range(len(routes_pool))
        ]
        
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



    def fixed_requests_must_be_in_solution_cosntr(self, model):
        for route_dict in self.fixed_routes_dict:
            for request in route_dict["requests"]:
                req_var = model.var_by_name("x_"+str(request))
                model.add_constr(
                    lin_expr=(req_var == 1),
                    name="x_"+str(request)+"_is_fixed"
                )


    def make_constraints(self, model, solution, routes_with_request, parameters):
        routes_pool = parameters["routes_pool"]

        # Request cannot repeat
        self.request_chosen(
            model, 
            routes_pool,
            routes_with_request 
        )
        
        # Limited Fleet
        self.limited_fleet_constr(model, routes_pool)

        # Routes Cost cannot be worser than a maximum percentage
        # self.routes_max_cost_constr(model, solution, routes_pool)

        # Fixed requests must be present
        self.fixed_requests_must_be_in_solution_cosntr(model)

        # for cons in model.constrs:
        #     print(cons)

    def all_vehicles_in_solution(self, new_solution):
        if (new_solution.number_of_routes() < self.fleet):
            return False
        return True

    
    def complete_number_of_vehicles(self, new_solution):
        while (new_solution.number_of_routes() < self.fleet):
            new_solution.add_route(Route())


    def construct_solution_from_model(self, model, parameters):
        routes_pool = parameters["routes_pool"]
        y = [
            model.var_by_name("y_"+str(i))
            for i in range(len(routes_pool))
        ]
        
        new_soltuion = self.construct_solution_from_chosen_routes(
            y, 
            routes_pool
        )
            

        if (not self.all_vehicles_in_solution(new_soltuion)):
            self.complete_number_of_vehicles(new_soltuion)

        return new_soltuion



    def get_attr_relation_reader(self):
        return {
            "fleet_size" : "fleet",
            "fixed_routes_dict" : "fixed_routes_dict"
        }