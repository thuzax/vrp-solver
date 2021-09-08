import json

from abc import ABC, ABCMeta, abstractmethod

from src import exceptions
from src.GenericClass import GenericClass
from src.objects_managers import *
from src.objects_creation_manager import create_class_by_name

class SolverClass(GenericClass, metaclass=ABCMeta):
    
    instance = None


    def __new__(cls, *args, **kwargs):
        for subcls in cls.__subclasses__():
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
            self.alternative_output_name = None
            self.output_type = None
            self.obj_func = None
            self.obj_func_name = None
            self.constraints_names = None
            self.constraints = None

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


    def write_final_data(self, running_data):
        if (self.output_path[-1] != "/"):
            self.output_path += "/"

        if (self.output_name == ""):
            self.output_name = self.alternative_output_name + "_sol"

        json_output_file_name = ""
        json_output_file_name += self.output_path 
        json_output_file_name += "running_data_"
        json_output_file_name += self.output_name 
        json_output_file_name += ".json"
        with open(json_output_file_name, "w") as output_file:
            output_file.write(json.dumps(running_data, indent=2))


    @abstractmethod
    def solve(self):
        pass


    def update_heuristics_data(self):
        pass


    @abstractmethod
    def write_file(self):
        pass

    @abstractmethod
    def get_attr_relation_reader_solver(self):
        return {
            "input_name" : "alternative_output_name"
        }