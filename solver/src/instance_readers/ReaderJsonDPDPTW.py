
from gc import freeze
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
        self.fixed_routes_dict = None

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
        self.fixed_routes_dict = self.read_fixed(fixed_requests)

        self.read_demands(dem)
        self.read_services_times(serv_times)
        self.read_time_windows(tws)
        


    def read_fixed(self, fixed_requests):
        fix_req = []
        pairs = []
        picks = []
        delis = []
        for route_dict in fixed_requests:
            fix_req.append(route_dict)
            fix_req[-1]["requests"] = set()
            route_fixed = route_dict["route"]
            for vertex_id in route_fixed:
                pair = (vertex_id, vertex_id + int(len(self.points)/2))
                if (pair[1] < len(self.points)):
                    fix_req[-1]["requests"].add(pair)
                    pairs.append(pair)
                    delis.append(pair[1])
                    picks.append(pair[0])
        
        self.requests = tuple(list(self.requests) + pairs)
        self.pickups = list(self.pickups) + picks
        self.deliveries = list(self.deliveries) + delis

        self.pickups.sort()
        self.deliveries.sort()

        self.pickups = set(self.pickups)
        self.deliveries = set(self.deliveries)

        self.number_of_requests = len(self.requests)

        return fix_req



    def create_specific_vertices(self):
        for route_fixed_dict in self.fixed_routes_dict:
            route_fixed_requests = route_fixed_dict["requests"]
            for item in route_fixed_requests:
                pick, deli = item
                self.create_vertex(pick)
                self.vertices_dict[pick].make_fixed()
                self.create_vertex(deli)
                self.vertices_dict[deli].make_fixed()
