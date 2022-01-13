import json

from abc import ABC, ABCMeta, abstractmethod
import time
from src.solution_check import get_solution_check_complete_data

from src import exceptions, execution_log, file_log
from src.GenericClass import GenericClass
from src.objects_managers import *
from src.objects_creation_manager import create_class_by_name

class SolverClass(GenericClass, metaclass=ABCMeta):
    
    instance = None

    def __new__(cls, *args, **kwargs):
        for subcls in GenericClass.get_all_subclasses(cls):
            if (subcls.instance is not None):
                return subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(SolverClass, cls).__new__(
                cls, *args, **kwargs
            )
        
        return cls.instance

    def __init__(self, solver_class_name):
        if (not hasattr(self, "name")):
            self.name = solver_class_name
            
            # Acquired from input
            self.output_path = None
            self.output_name = None
            self.output_type = None

            self.obj_func = None
            self.obj_func_name = None
            
            self.constraints_names = None
            self.constraints = None

            self.construction_name = None
            self.construction = None
            
            self.metaheuristic_name = None
            self.metaheuristic = None

            self.best_solution = None

            self.initialize_class_attributes()


    def route_is_feasible(self, route):
        for constraint in self.constraints:
            if (not constraint.route_is_feasible(route)):
                return False
        
        return True

    def solution_is_feasible(self, solution):
        for constraint in self.constraints:
            if (not constraint.solution_is_feasible(solution)):
                return False

        return True


    def initialize_objective(self):
        objective_class_name = list(self.obj_func.keys())[0]
        self.obj_func = create_class_by_name(
            objective_class_name, 
            self.obj_func[objective_class_name]
        )


    def create_heuristic_obj(self, class_name, class_data):
        heuristic_obj = create_class_by_name(
            class_name,
            class_data
        )
        
        obj_func_class_name = list(class_data["obj_func"].keys())[0]
        obj_func_class_data = class_data["obj_func"][obj_func_class_name]
        obj_func_object = create_class_by_name(
            obj_func_class_name, 
            obj_func_class_data
        )

        heuristic_obj.obj_func = obj_func_object

        return heuristic_obj


    @abstractmethod
    def solve(self):
        pass


    def update_and_get_best_after_timeout(self):
        file_log.add_warning_log("Searching current best solution.")
        if (self.best_solution is None):
            file_log.add_warning_log("Could not create any solution.")
            return None
        
        obj_value = self.obj_func.get_solution_cost(self.best_solution)
        routes_cost = self.obj_func.get_routes_sum_cost(
            self.best_solution.routes
        )

        self.best_solution.set_objective_value(obj_value)
        self.best_solution.set_routes_cost(routes_cost)
    
        metaheuristic_solution = self.metaheuristic.get_current_best_solution()

        if (metaheuristic_solution is not None):
            meta_obj_value = self.obj_func.get_solution_cost(
                metaheuristic_solution
            )
            meta_routes_cost = self.obj_func.get_routes_sum_cost(
                metaheuristic_solution.routes
            )

            metaheuristic_solution.set_objective_value(meta_obj_value)
            metaheuristic_solution.set_routes_cost(meta_routes_cost)

        else:
            file_log.add_warning_log(
                "Metaheuristic could not find any solution."
            )
        meta_is_better = (
            self.solution_is_feasible(metaheuristic_solution)
            and 
            self.obj_func.solution_is_better(
                metaheuristic_solution, 
                self.best_solution
            )
        )
        if (meta_is_better):
            self.best_solution = metaheuristic_solution

        file_log.add_warning_log("Current best solution found.")
        self.print_best_solution()
        return self.best_solution


    def get_best_solution(self):
        return self.best_solution


    def print_best_solution(self):
        print(self.best_solution)


    def get_best_solution_dict(self):
        if (self.best_solution is None):
            return None
        return self.best_solution.get_dict()


    def print_solution_verification(self, solution, exec_time):
        print("..........................................")
        print("..........................................")
        print("SOLUTION VERIFICATION")
        print("..........................................")
        print("..........................................")
        if (solution is None):
            execution_log.warning_log("Solution is None")
            return

        print(
            get_solution_check_complete_data(
                solution, 
                self.constraints, 
                self.obj_func
            )
        )
        print(
            "best obj, best route_cost:", 
            solution.cost(),
            ",",
            solution.routes_cost()
        )
        print("Total time:", exec_time)


    def update_heuristics_data(self):
        pass


    @abstractmethod
    def get_attr_relation_reader_solver(self):
        return {
            "input_name" : "output_name"
        }


    @staticmethod
    def clear():
        for subcls in SolverClass.__subclasses__():
            subcls.instance = None
        SolverClass.instance = None