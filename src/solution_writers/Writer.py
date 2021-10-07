from abc import ABC, ABCMeta, abstractmethod
from src.instance_readers import Reader
from src.vertex_classes import Vertex

from src import file_log

from src import exceptions
from src.GenericClass import GenericClass

from pprint import pprint


class Writer(GenericClass, metaclass=ABCMeta):


    instance = None

    def __new__(cls, *args, **kwargs):
        for subcls in cls.__subclasses__():
            if (subcls.instance is not None):
                return subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(Writer, cls).__new__(
                cls, *args, **kwargs
            )
        
        return cls.instance


    def __init__(self, writer_class_name):
        if (not hasattr(self, "name")):
            self.name = writer_class_name
            self.output_path = None
            self.output_name = None
            self.output_type = None
            self.initialize_class_attributes()

    def get_output_file_name(self):
        if (self.output_path is None):
            self.output_path = Reader().input_path

        if (self.output_path[-1] != "/"):
            self.output_path = self.output_path + "/"

        if (self.output_name is None):
            self.output_name = Reader().input_name


        return self.output_path + self.output_name


    def write_log(self):
        if (not file_log.do_file_log()):
            return

        log_data = file_log.get_log_text()
        
        output_file_name = self.get_output_file_name() + "_log.txt"
        
        with open(output_file_name, "w") as out_file:
            out_file.write(log_data)


    def write_solution(self, solution):
        output_file_name = self.get_output_file_name() + "_sol."
        
        if (self.output_type is not None):
            output_file_name += self.output_type
        else:
            output_file_name += "txt"



        self.write_solution_specific(output_file_name, solution)


    @abstractmethod
    def write_solution_specific(self, output_file_name, solution):
        pass
