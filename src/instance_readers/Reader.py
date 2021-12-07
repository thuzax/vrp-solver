from abc import ABC, ABCMeta, abstractmethod
from src.vertex_classes import Vertex

from src.instance_readers.Reader import *
from src import exceptions
from src.GenericClass import GenericClass

from pprint import pprint


class Reader(GenericClass, metaclass=ABCMeta):


    instance = None
    
    ### Obrigatory for all Porblems ###
    

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
            
            self.input_path = None
            self.input_name = None
            self.input_type = "json"

            self.number_of_requests = None
            self.vertices = []
            self.vertices_dict = {}

            self.initialize_class_attributes()


    def create_vertex(self, vertex_id):
        vertex = Vertex()
        vertex.set_attribute("vertex_id", vertex_id)
        
        rela_attr = Vertex.get_reader_vertex_attr_relation()
        for reader_attr_name, vertex_attr_name in rela_attr.items():
            reader_attr = getattr(self, reader_attr_name)
            vertex.set_attribute(vertex_attr_name, reader_attr[vertex_id])

        self.vertices_dict[vertex_id] = vertex


    @abstractmethod
    def create_depots(self, request_position):
        pass


    def create_vertices(self):
        self.create_depots()
        for request_position in range(self.number_of_requests):
            self.create_request_vertex(request_position)

        self.vertices = [None for i in range(len(self.vertices_dict))]

        for key, value in self.vertices_dict.items():
            self.vertices[key] = value

    
    def get_file_name(self):
        if (self.input_path[-1] != "/"):
            self.input_path = self.input_path + "/"
        
        file_name = self.input_path + self.input_name + "." + self.input_type
        
        return file_name


    def read_input_file(self):
        file_name = self.get_file_name()
        self.read_specific_input(file_name)
        self.create_vertices()

        


    @abstractmethod
    def read_specific_input(self, file_name):
        pass

    @staticmethod
    def clear():
        for subcls in Reader.__subclasses__():
            subcls.instance = None
        Reader.instance = None