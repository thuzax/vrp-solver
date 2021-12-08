
import json
from src.vertex_classes import Vertex
import numpy
import math

from src.instance_readers.ReaderJsonPDPTW import ReaderJsonPDPTW

class ReaderJsonDPDPTW(ReaderJsonPDPTW):
    
    def __init__(self):
        super().__init__()
    
    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        # From input File
        self.fixed = None

    def read_specific_input(self, file_name):        
        with open(file_name, "r") as input_file:
            input_text = input_file.read()
            input_dict = json.loads(input_text)
    
            points_dict = input_dict["points"]
            n_points = input_dict["number_of_points"]
            dist_mat = input_dict["distance_matrix"]
            time_mat = input_dict["time_matrix"]
            cap = input_dict["capacity"]
            pds = input_dict["pickups_and_deliveries"]
            dem = input_dict["demands"]
            serv_times = input_dict["services_times"]
            tws = input_dict["time_windows_pd"]
            planning_horizon = input_dict["planning_horizon"]
            time_windows_size = input_dict["time_windows_size"]

            fixed_points = input_dict["fixed"]

        self.capacity = int(cap)
        self.planning_horizon = int(planning_horizon)
        
        if (time_windows_size is not None):
            self.time_windows_size = int(time_windows_size)

        self.read_points(points_dict, n_points)
        self.distance_matrix = self.read_matrix(dist_mat)
        self.time_matrix = self.read_matrix(time_mat)
        self.read_pickups_and_deliveries(pds)
        self.read_demands(dem)
        self.read_services_times(serv_times)
        self.read_time_windows(tws)
        
        self.fixed = fixed_points
    

    def create_specific_vertices(self):
        for route_fixed_vertices in self.fixed:
            for point in route_fixed_vertices:
                self.create_vertex(point)
                self.vertices_dict[point].make_fixed()

