
import copy

from src.vertex_classes import VertexPDPTW

class VertexDPDPTW(VertexPDPTW):

    def __init__(self):
        super().__init__()


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.is_fixed = False

    def __str__(self):
        text = super().__str__()
        text += "IS FIXED? " + str(self.is_fixed) + "\n"
        return text


    def make_fixed(self):
        self.is_fixed = True
