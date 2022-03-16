
import copy

from src.vertex_classes import VertexDPDPTW

class VertexDPDPTWHeterogeneousFleet(VertexDPDPTW):

    def __init__(self):
        super().__init__()


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.attendance_type = None


    def set_attendance_type(self, attendance_type):
        self.attendance_type = attendance_type

    def get_attendance_type(self):
        return self.attendance_type
    
    def __str__(self):
        text = super().__str__()
        text += "ATT TYPE: " + str(self.attendance_type)
        return text


