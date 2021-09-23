from abc import ABCMeta, abstractmethod
from src.GenericClass import GenericClass


class AcceptanceHeuristic(GenericClass, metaclass=ABCMeta):

    def __init__(self, name):
        self.name = name
        self.initialize_class_attributes()

    @abstractmethod
    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    @abstractmethod
    def accept(self, new_solution, obj_func=None, parameters=None):
        pass

    @abstractmethod
    def get_attr_relation_reader_accept_heuri(self):
        pass