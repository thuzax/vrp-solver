
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

            fixed_requests = input_dict["fixed"]

        
        self.capacity = int(cap)
        self.planning_horizon = int(planning_horizon)
        
        if (time_windows_size is not None):
            self.time_windows_size = int(time_windows_size)

        self.read_points(points_dict, n_points)
        self.distance_matrix = self.read_matrix(dist_mat)
        self.time_matrix = self.read_matrix(time_mat)
        
        self.read_pickups_and_deliveries(pds)
        self.fixed = self.read_fixed(fixed_requests)

        self.read_demands(dem)
        self.read_services_times(serv_times)
        self.read_time_windows(tws)
        


    def read_fixed(self, fixed_requests):
        fix_req = []
        pairs = []
        picks = []
        delis = []
        for route_fixed in fixed_requests:
            fix_req.append([])
            for pair in route_fixed:
                pair = tuple(pair)
                fix_req[-1].append(pair)
                pairs.append(pair)
                delis.append(pair[1])
                picks.append(pair[0])

        self.requests = tuple(list(self.requests) + pairs)
        self.pickups = list(self.pickups) + picks
        self.deliveries = list(self.deliveries) + delis

        self.pickups.sort()
        self.deliveries.sort()

        self.pickups = tuple(self.pickups)
        self.deliveries = tuple(self.deliveries)

        self.number_of_requests = len(self.requests)

        return fix_req



    def create_specific_vertices(self):
        for route_fixed_vertices in self.fixed:
            for item in route_fixed_vertices:
                pick, deli = item
                self.create_vertex(pick)
                self.vertices_dict[pick].make_fixed()
                self.create_vertex(deli)
                self.vertices_dict[deli].make_fixed()

