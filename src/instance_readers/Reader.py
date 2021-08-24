from abc import ABC, ABCMeta, abstractmethod

from src.instance_readers.Reader import *
from src import exceptions
from src.GenericClass import GenericClass


class Reader(GenericClass, metaclass=ABCMeta):


    instance = None
    
    ### Obrigatory for all Porblems ###
    
    # Acquired from configuration file
    input_path = None
    input_name = None
    input_type = "json"


    def __new__(cls, *args, **kwargs):
        for subcls in cls.__subclasses__():
            if (subcls.instance is not None):
                return subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(Reader, cls).__new__(
                cls, *args, **kwargs
            )
        
        return cls.instance

    def __init__(self, reader_class_name):
        if (not hasattr(self, "name")):
            self.name = reader_class_name
            self.initialize_class_attributes()


    # def set_attribute(self, name, value):
    #     if (not hasattr(self, name)):
    #         raise exceptions.ObjectDoesNotHaveAttribute(
    #             self.__class__.__name__, 
    #             name
    #         )
            
    #     self.__setattr__(name, value)


    def read_input_file(self):
        
        if (self.input_path[-1] != "/"):
            self.input_path = self.input_path + "/"
        
        file_name = self.input_path + self.input_name + "." + self.input_type

        self.read_specific_input(file_name)
        


    @abstractmethod
    def read_specific_input(self, file_name):
        pass

