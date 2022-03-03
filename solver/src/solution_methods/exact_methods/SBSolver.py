import time
from mip import *
from abc import ABCMeta, abstractmethod

from src import file_log

from src.solution_methods.SolutionMethod import SolutionMethod



class SBSolver(SolutionMethod, metaclass=ABCMeta):
    
    def __init__(self, name):
        super().__init__(name)


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.solver_code = None
        self.opt_time_limit = None


    def get_current_best_solution(self):
        return super().get_current_best_solution()


    @abstractmethod
    def make_model_obj_func(self, model, parameters):
        pass


    def create_model(self):
        return Model(
            name="Set Partitioning", 
            sense=MINIMIZE,
            solver_name=self.solver_code
        )


    def get_request_in_route_dict(self, parameters):
        requests = parameters["requests_set"]
        routes_pool = parameters["routes_pool"]
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

        return request_in_route



    @abstractmethod
    def create_variables(self, model, parameters):
        pass

    @abstractmethod
    def initialize_model(self, model, solution, parameters):
        pass

    
    @abstractmethod
    def make_constraints(self, model, solution, request_in_route, parameters):
        pass
    

    def run_model(self, model):
        status = model.optimize(max_seconds=self.opt_time_limit)
        found_feasible = False
        
        if status == OptimizationStatus.OPTIMAL:
            found_feasible = True
        elif status == OptimizationStatus.FEASIBLE:
            found_feasible = True
        
        return found_feasible

    @abstractmethod
    def construct_solution_from_model(self, model, parameters):
        pass


    def construct_model(self, solution, parameters):
        """Construct a ILP

        Args:
            solution (Solution: An initial for the ILP
            parameters {dict}: A dictionary with additional parameters

        Returns:
            mip.Model: A ILP
            list of mip.Var: List with ILP varibles
        """

        self.best_solution = None

        model = self.create_model()
        
        self.create_variables(model, parameters)

        request_in_route = self.get_request_in_route_dict(parameters)
        self.make_constraints(model, solution, request_in_route, parameters)

        self.make_model_obj_func(model, parameters)
        
        self.initialize_model(model, solution, parameters)

        return model



    def solve(self, solution, parameters):
        self.best_solution = None

        start_time = time.time()
        model = self.construct_model(solution, parameters)
        found_feasible = self.run_model(model)

        new_soltuion = None
        if (found_feasible):
            new_soltuion = self.construct_solution_from_model(
                model,
                parameters
            )

        if (new_soltuion is not None):
            self.best_solution = new_soltuion
            message = "PartitionMaxRequests" + "\n"
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
