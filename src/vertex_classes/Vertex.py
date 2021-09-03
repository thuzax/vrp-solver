import numpy

from abc import ABC, ABCMeta, abstractmethod

from src import exceptions
from src.GenericClass import GenericClass


class VertexSubClass:
    instance = None
    vertex_subclass = None
    vertex_subclass_params = None

    def __new__(cls, *args, **kwargs):
        if (len(cls.__subclasses__())):
            raise exceptions.ClassCannotBeInherited("VertexSubClass")

        if (cls.instance is None):
            cls.instance = super(VertexSubClass, cls).__new__(cls)

        return cls.instance


    def __init__(self, subclass=None):
        if (subclass is not None):
            self.vertex_subclass = subclass


create_super = False
class Vertex(GenericClass, metaclass=ABCMeta):

    child_created = False

    def __new__(cls, *args, **kwargs):
        global create_super
        
        if (create_super):
            cls = super(Vertex, cls).__new__(cls, *args, **kwargs)
            create_super = False
            return cls
        
        create_super = True
        cls = VertexSubClass().vertex_subclass()
        cls.child_created = True
        return cls


    def __init__(self, vertex_class_name=None):
        if (not hasattr(self, "name")):
            self.name = vertex_class_name
            self.vertex_id = None

            self.initialize_class_attributes()
            self.set_input_params

    def __str__(self):
        return str(self.vertex_id)


    def set_input_params(self):
        vertex_input_params = VertexSubClass.vertex_subclass_params
        if (vertex_input_params is None):
            return
        for param_name, param_value in vertex_input_params.items():
            self.set_attribute(param_name, param_value)
            


    @staticmethod
    @abstractmethod
    def get_attr_relation_reader_vertex():
        pass


    @staticmethod
    def get_reader_vertex_attr_relation():
        vertex_subclass = VertexSubClass().vertex_subclass
        reader_vertex_attr = vertex_subclass.get_attr_relation_reader_vertex()
        return reader_vertex_attr


    @staticmethod
    def update_vertex_class_params(params):
        VertexSubClass.vertex_subclass_params = params
