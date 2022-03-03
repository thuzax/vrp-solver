
from gc import freeze
import json
from src.vertex_classes import Vertex
import numpy
import math

from src.instance_readers.ReaderJsonDPDPTW import ReaderJsonDPDPTW

class ReaderJsonDPDPTWLimitedFleet(ReaderJsonDPDPTW):


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fleet_size = None

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

            fixed_requests = input_dict["fixed"]

            fleet_size = input_dict["fleet_size"]

        
        self.capacity = int(cap)
        self.planning_horizon = int(planning_horizon)
        
        if (time_windows_size is not None):
            self.time_windows_size = int(time_windows_size)

        self.read_points(points_dict, n_points)
        self.distance_matrix = self.read_matrix(dist_mat)
        self.time_matrix = self.read_matrix(time_mat)
        
        self.fleet_size = self.read_fleet_size(fleet_size)

        self.read_pickups_and_deliveries(pds)
        self.fixed_routes_dict = self.read_fixed(fixed_requests)

        self.read_demands(dem)
        self.read_services_times(serv_times)
        self.read_time_windows(tws)


    def read_fleet_size(self, fleet_size):
        return int(fleet_size)
