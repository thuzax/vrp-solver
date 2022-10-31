
import copy

from src.vertex_classes import VertexPDPTW

class VertexDPDPTW(VertexPDPTW):

    def __init__(self):
        super().__init__()


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fixed = False

    def make_fixed(self):
        self.fixed = True


    def is_fixed(self):
        return self.fixed

    
    def __str__(self):
        text = super().__str__()
        text += "IS FIXED? " + str(self.fixed) + "\n"
        return text


