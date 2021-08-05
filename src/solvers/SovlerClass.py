import json

from abc import ABC, abstractmethod

from src import exceptions


class SolverClass(ABC):
    
    instance = None
    
    ### Obrigatory for all Porblems ###
    
    # Acquired from configuration file
    output_path = None
    output_name = None
    output_type = "json"
    
    # Acquired while running


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
        self.name = solver_class_name


    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                self.__class__.__name__, 
                name
            )
            
        self.__setattr__(name, value)


    def write_file(self):
        pass


    def write_final_data(self, running_data):
        if (self.output_path[-1] != "/"):
            self.output_path += "/"

        json_output_file_name = ""
        json_output_file_name += self.output_path 
        json_output_file_name += "running_data_"
        json_output_file_name += self.output_name 
        json_output_file_name += ".json"
        with open(json_output_file_name, "w") as output_file:
            output_file.write(json.dumps(running_data, indent=2))
