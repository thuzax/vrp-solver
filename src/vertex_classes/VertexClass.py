import numpy

from abc import ABC, ABCMeta, abstractmethod

from src import exceptions
from src.GenericClass import GenericClass

class VertexClass(GenericClass, metaclass=ABCMeta):
    def __init__(self, vertex_class_name):
        if (not hasattr(self, "name")):
            self.name = vertex_class_name
            self.vertex_id = None

            self.initialize_class_attributes()

    def __str__(self):
        return str(self.vertex_id)

    @staticmethod
    @abstractmethod
    def get_attr_relation_reader_vertex():
        pass
