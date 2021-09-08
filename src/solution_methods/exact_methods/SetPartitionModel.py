from mip import *
from src.solution_methods.SolutionMethod import SolutionMethod

class SetPartitionModel(SolutionMethod):
    
    def __init__(self):
        if (not hasattr(self, "name")):
            super().__init__("SetPartitionModel")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.solver_code = None
        self.opt_time_limit = None


    def solve(self, solution, parameters):
        requests = parameters["requests"]
        # list of routes
        routes_pool = parameters["routes_pool"]

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
                request_in_route.remove(request)


        y = [
                model.add_var(
                    var_type=BINARY, 
                    name="y_"+str(i)
                )
                for i in range(len(routes_pool))
            ]

        for request in request_in_route:
            n_routes_sum = (
                request_in_route[request][i] * y[i] 
                for i in range(len(routes_pool))
            )
            model.add_constr(
                n_routes_sum == 1, 
                name="one_attendance_"+str(request)
            )
        
        model.objective = xsum(
            routes_pool[i].cost() * y[i]
            for i in range(len(routes_pool))
        )
        
        status = model.optimize(max_seconds=self.opt_time)
        found_feasible = False
        if status == OptimizationStatus.OPTIMAL:
            print("Optimal")
            found_feasible = True
        elif status == OptimizationStatus.FEASIBLE:
            print("Feasible")
            print(model.objective_value, model.objective_bound)
            found_feasible = True
        elif status == OptimizationStatus.NO_SOLUTION_FOUND:
            print("No feasible solution found")

        if (found_feasible):
            for i in range(len(routes_pool)):
                if (y[i]):
                    print(routes_pool[i])


    def update_route_values(self, route, position, request):
        super().update_route_values(route, position, request)


    def get_attr_relation_reader_heuristic(self):
        rela_reader_heur = super().get_attr_relation_reader_heuristic()
        return rela_reader_heur
