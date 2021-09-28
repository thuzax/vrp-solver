import time
from mip import *

from src import file_log

from src.solution_classes.Solution import Solution
from src.solution_methods.SolutionMethod import SolutionMethod

class SetPartitionModel(SolutionMethod):
    
    def __init__(self):
        if (not hasattr(self, "name")):
            super().__init__("SetPartitionModel")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.solver_code = None
        self.opt_time_limit = None

    
    def get_current_best_solution(self):
        return super().get_current_best_solution()


    def solve(self, solution, parameters):
        requests = parameters["requests_set"]
        # list of routes
        routes_pool = parameters["routes_pool"]

        self.best_solution = None

        start_time = time.time()
        model = Model(
            name="Set Partitioning", 
            sense=MINIMIZE,
            solver_name=self.solver_code
        )

        request_in_route = {}
        
        for request in requests:
            request_in_route[request] = {}
            request_has_at_least_one_route = False
            for pos, route in enumerate(routes_pool):
                if (request in route):
                    request_in_route[request][pos] = 1
                    request_has_at_least_one_route = True
                else:
                    request_in_route[request][pos] = 0
            
            if (not request_has_at_least_one_route):
                request_in_route.pop(request)

        y = [
                model.add_var(
                    var_type=BINARY, 
                    name="y_"+str(i)
                )
                for i in range(len(routes_pool))
            ]

        initial_routes_pos = set()
        for i, route_1 in enumerate(routes_pool):
            for route_2 in solution.routes:
                if (route_1.is_equal(route_2)):
                    initial_routes_pos.add(i)

        model.start = [
            (y[i], 1 if i in initial_routes_pos else 0) 
            for i in range(len(routes_pool))
        ]

        for request in request_in_route:
            n_routes_sum = xsum(
                request_in_route[request][i] * y[i] 
                for i in range(len(routes_pool))
            )
            model.add_constr(
                lin_expr=(n_routes_sum == 1), 
                name="one_attendance_"+str(request)
            )
        
        model.objective = xsum(
            routes_pool[i].cost() * y[i]
            for i in range(len(routes_pool))
        )

        status = model.optimize(max_seconds=self.opt_time_limit)
        found_feasible = False
        if status == OptimizationStatus.OPTIMAL:
            found_feasible = True
        elif status == OptimizationStatus.FEASIBLE:
            print(model.objective_value, model.objective_bound)
            found_feasible = True

        new_soltuion = None
        if (found_feasible):
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

        if (new_soltuion is not None):
            self.best_solution = new_soltuion
            message = "SetPartitioningModel" + "\n"
            message += "Exec Time: " + str(time.time() - start_time)
            message += "\n"
            if (self.obj_func.solution_is_better(new_soltuion, solution)):
                message += "Improved"
            file_log.add_solution_log(self.best_solution, message)
            return new_soltuion
        
        message = self.__class__.__name__ + "did not find a feasible solution."
        file_log.add_warning_log(message)
        return solution

    def update_route_values(self, route, position, request):
        super().update_route_values(route, position, request)


    def get_attr_relation_reader_heuristic(self):
        rela_reader_heur = super().get_attr_relation_reader_heuristic()
        return rela_reader_heur
