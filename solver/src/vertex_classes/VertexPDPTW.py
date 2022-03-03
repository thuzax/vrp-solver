
import copy

from src.vertex_classes import VertexClass


class VertexPDPTW(VertexClass):

    def __init__(self):
        super().__init__("Route PDPTW")


    def initialize_class_attributes(self):
        self.coords = None
        self.service_time = None
        self.time_window = None
        self.demand = None

    @staticmethod
    def get_attr_relation_reader_vertex():
        reader_route_attr_rela = {
            "points" : "coords",
            "services_times" : "service_time",
            "time_windows" : "time_window",
            "demands" : "demand",
        }
        
        return reader_route_attr_rela

    def __str__(self):
        text = ""
        text += "ID: " + str(self.vertex_id) + "\n"
        text += "POINT: " + str(self.coords) + "\n"
        text += "DEMAND: " + str(self.demand) + "\n"
        text += "SERVICE TIME: " + str(self.service_time) + "\n"
        text += "TIME WINDOW: " + str(self.time_window) + "\n"
        return text
