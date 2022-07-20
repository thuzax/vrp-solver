import time
from mip import *
from abc import ABCMeta, abstractmethod
from src import execution_log
from src.solution_classes import Solution

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
    def make_model_obj_func(self, model, solution, parameters):
        pass


    def create_model(self):
        return Model(
            name="Set Partitioning", 
            sense=MINIMIZE,
            solver_name=self.solver_code
        )


    def get_routes_with_request_dict(self, parameters):
        requests = parameters["requests_set"]
        routes_pool = parameters["routes_pool"]
        routes_with_request = {}
        for request in requests:
            routes_with_request[request] = []
            request_has_at_least_one_route = False
            for pos, route in enumerate(routes_pool):
                if (request in route):
                    routes_with_request[request].append(pos)
                    request_has_at_least_one_route = True
            
            if (not request_has_at_least_one_route):
                routes_with_request.pop(request)

        return routes_with_request



    @abstractmethod
    def create_variables(self, model, parameters):
        pass

    @abstractmethod
    def initialize_model(self, model, solution, parameters):
        pass

    
    @abstractmethod
    def make_constraints(
        self, 
        model, 
        solution, 
        routes_with_request, 
        parameters
    ):
        pass
    

    def run_model(self, model):
        status = model.optimize(max_seconds=self.opt_time_limit)
        found_feasible = False
        
        if status == OptimizationStatus.OPTIMAL:
            found_feasible = True
        elif status == OptimizationStatus.FEASIBLE:
            found_feasible = True
        else:
            print("INFEASIBLE")
            # print("INFEASIBLE")
            # print("INFEASIBLE")
            # print("INFEASIBLE")

        return found_feasible


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

        routes_with_request = self.get_routes_with_request_dict(parameters)
        self.make_constraints(model, solution, routes_with_request, parameters)

        self.make_model_obj_func(model, solution, parameters)
        
        self.initialize_model(model, solution, parameters)

        return model

    @abstractmethod
    def construct_solution_from_model(self, model, parameters):
        y = model.vars
        routes_pool = parameters["routes_pool"]
        new_soltuion = self.construct_solution_from_chosen_routes(
            y, 
            routes_pool
        )
        return new_soltuion


    def construct_solution_from_chosen_routes(self, y, routes_pool):
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

        return new_soltuion


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
            new_soltuion.set_objective_value(
                self.obj_func.get_solution_cost(new_soltuion)
            )
            new_soltuion.set_routes_cost(
                self.obj_func.get_routes_sum_cost(new_soltuion.routes())
            )
            # print("+++++++++++++")
            # print(new_soltuion.cost())
            # print(new_soltuion.routes_cost())

        if (new_soltuion is not None):
            self.best_solution = new_soltuion
            message = self.name + "\n"
            message += "Exec Time: " + str(time.time() - start_time)
            message += "\n"
            if (self.obj_func.solution_is_better(new_soltuion, solution)):
                message += "Improved"
            file_log.add_solution_log(self.best_solution, message)
            return new_soltuion
        
        message = self.__class__.__name__ + "did not find a feasible solution."
        file_log.add_warning_log(message)
        execution_log.warning_log(message)
        return solution


    def get_attr_relation_reader_heuristic(self):
        rela_reader_heur = super().get_attr_relation_reader_heuristic()
        return rela_reader_heur
