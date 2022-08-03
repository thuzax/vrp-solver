from os import stat
from src.GenericClass import GenericClass
from src import exceptions

class Vertex(GenericClass):
    instance = None
    
    vertex_cls = None
    reader_vertex_attr = None


    def __new__(cls, *args, **kwargs):
        if (len(cls.__subclasses__())):
            raise exceptions.ClassCannotBeInherited("Vertex")
        
        if (cls.instance is None):
            cls.instance = super(Vertex, cls).__new__(cls)
        
        vertex = cls.vertex_cls()
        
        return vertex

    def __init__(self):
        if (not hasattr(self, "vertex_cls")):
            self.initialize_class_attributes()

    @staticmethod
    def set_class(vertex_cls):
        Vertex.vertex_cls = vertex_cls
        Vertex.reader_vertex_attr = (
            Vertex.vertex_cls.get_attr_relation_reader()
        )

    def initialize_class_attributes(self):
        return super().initialize_class_attributes()

    @staticmethod
    def get_reader_vertex_attr_relation():
        return Vertex.reader_vertex_attr
    

    def clear():
        for subcls in Vertex.__subclasses__():
            subcls.instance = None
            subcls.vertex_cls = None
            subcls.reader_vertex_attr = None
        Vertex.instance = None
        Vertex.vertex_cls = None
        Vertex.reader_vertex_attr = None