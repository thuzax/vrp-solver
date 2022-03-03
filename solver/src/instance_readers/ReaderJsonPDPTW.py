
import json
from src.vertex_classes import Vertex
import numpy
import math

from src.instance_readers.Reader import Reader

class ReaderJsonPDPTW(Reader):
    
    def __init__(self):
        super().__init__("PDPTW json input file Reader")
    
    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        # From input File
        self.points = None
        self.number_of_points = None
        self.distance_matrix = None
        self.time_matrix = None
        self.capacity = None
        self.demands = None
        self.services_times = None
        self.time_windows = None
        self.planning_horizon = None
        self.time_windows_size = None

        # Generated based on input File
        self.depot = None
        self.pickups = None
        self.deliveries = None
        self.requests = None
        self.relatedness_measure = None

        self.has_depot = None

        self.phi = None
        self.qui = None
        self.psi = None

    
    def read_points(self, points_dict, n_points):
        self.has_depot = (n_points % 2 == 1)
        points = []

        start_index = 0
        if (not self.has_depot):
            start_index = 1

        for i in range(start_index, n_points+start_index):
            points.append(points_dict[str(i)])

        self.number_of_points = n_points
        
        # depot is considered 0
        self.depot = 0
        # if doesn't have a origini
        if (not self.has_depot):
            #  add fake depot
            self.points = numpy.array(
                [[None, None]] + points, 
                dtype=float
            )
            self.number_of_points += 1

        else:
            self.points = numpy.array(points, dtype=float)
        


    def read_matrix(self, matrix_dict):

        matrix = [
            [
                0
                for i in range(self.number_of_points)
            ]
            for i in range(self.number_of_points)
        ]

        start_index = 0
        if (not self.has_depot):
            start_index = 1

        for i in range(start_index, self.number_of_points):
            for j in range(start_index, self.number_of_points):
                matrix[i][j] = int(matrix_dict[str(i)][str(j)])

        # matrix = tuple(map(tuple, matrix))
        matrix = numpy.array(matrix)

        return matrix


    def read_pickups_and_deliveries(self, pds):
        self.number_of_requests = len(pds)
        # pickups = first half of points
        self.pickups = numpy.array(
            [r[0] for r in pds], 
            dtype=int
        )

        # deliveries = second half of points
        self.deliveries = numpy.array(
            [r[1] for r in pds], 
            dtype=int
        )
        self.requests = tuple([
            (self.pickups[i], self.deliveries[i])
            for i in range(len(pds))
        ])

        self.pickups = set(tuple(self.pickups))
        self.deliveries = set(tuple(self.deliveries))


    def read_demands(self, dem):
        self.demands = numpy.zeros((len(self.points)), dtype=int)

        self.demands[self.depot] = 0

        for pickup, delivery in self.requests:
            self.demands[pickup] = dem[str(pickup)]
            if (self.demands[delivery] > 0):
                self.demands[delivery] = -dem[str(delivery)]
            else:
                self.demands[delivery] = dem[str(delivery)]
        
        self.demands = tuple(self.demands)


    def read_services_times(self, serv_times):
        self.services_times = numpy.zeros(len(self.points), dtype=int)

        self.services_times[self.depot] = 0
        
        for pickup, delivery in self.requests:
            self.services_times[pickup] = serv_times[str(pickup)]
            self.services_times[delivery] = serv_times[str(delivery)]
        
        self.services_times = tuple(self.services_times)


    def read_time_windows(self, tws):
        
        self.time_windows = numpy.zeros(
            shape=(self.number_of_points, 2),
            dtype=int
        )

        self.time_windows[self.depot][0] = 0
        self.time_windows[self.depot][1] = self.planning_horizon

        
        for pickup, delivery in self.requests:
            self.time_windows[pickup][0] = tws[str(pickup)][0]
            self.time_windows[pickup][1] = tws[str(pickup)][1]
            self.time_windows[delivery][0] = tws[str(delivery)][0]
            self.time_windows[delivery][1] = tws[str(delivery)][1]

        self.time_windows = tuple(map(tuple, self.time_windows))

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
    

    def create_request_vertex(self, request_position):
        request = self.requests[request_position]
        pickup, delivery = request

        self.create_vertex(pickup)
        self.create_vertex(delivery)


    def create_depots(self):
        self.create_vertex(self.depot)


    def create_specific_vertices(self):
        pass