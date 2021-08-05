
import json
import numpy
import math

from src.instance_readers.Reader import Reader

class ReaderJsonPDPTW(Reader):
    
    # From input File
    points = None
    number_of_points = None
    distance_matrix = None
    time_matrix = None
    capacity = None
    demands = None
    services_times = None
    time_windows = None
    planning_horizon = None
    time_windows_size = None

    # Generated based on input File
    origin = None
    pickups = None
    deliveries = None

    has_origin = None

    def __init__(self):
        super().__init__("PDPTW json input file Reader")
    
    
    def read_points(self, points_dict, n_points, origin=None):
        self.has_origin = (origin is not None)
        points = []
        index_increment = 0

        if (not self.has_origin):
            index_increment = 1
        
        for i in range(n_points):
            points.append(points_dict[str(i + index_increment)])

        # if doesn't have a origini
        if (not self.has_origin):
            #  add origin
            self.points = numpy.array(
                [[None, None]] + points, 
                dtype=float
            )
            self.number_of_points = n_points + 1
            self.origin = 0
        else:
            # otherwise consider origin the point in position 0
            self.points = numpy.array(points, dtype=float)
            self.number_of_points = n_points
            self.origin = origin
        

    
    def read_matrix(self, matrix_dict):
        matrix = numpy.zeros(
            shape=(self.number_of_points, self.number_of_points), 
            dtype=int
        )
        index_increment = 0

        if (not self.has_origin):
            index_increment = 1

        for i in range(index_increment, self.number_of_points):
            for j in range(index_increment, self.number_of_points):
                matrix[i][j] = int(matrix_dict[str(i)][str(j)])

        return matrix


    def read_pickups_and_deliveries(self, pds):
        # pickups = origin + first half of points
        self.pickups = numpy.array(
            [i for i in range(1, len(pds)+1)], 
            dtype=int
        )

        # deliveries = origin + second half of points
        self.deliveries = numpy.array(
            [i + 1 + len(pds) for i in range(len(pds))], 
            dtype=int
        )


    def read_demands(self, dem):
        self.demands = numpy.zeros(len(self.pickups), dtype=int)

        for i in range(len(self.pickups)):
            self.demands[i] = dem[str(i+1)]


    def read_services_times(self, serv_times):
        self.services_times = numpy.zeros(len(self.points), dtype=int)

        self.services_times[self.origin] = 0

        index_increment = 0
        if (not self.has_origin):
            index_increment = 1
        
        for i in range(index_increment, len(self.points)):
            self.services_times[i] = serv_times[str(i)]


    def read_time_windows(self, tws):
        self.time_windows = numpy.zeros(
            shape=(self.number_of_points, 2),
            dtype=int
        )

        self.time_windows[self.origin][1] = self.planning_horizon

        if (not self.has_origin):
            index_increment = 1
        
        for i in range(index_increment, len(self.points)):
            self.time_windows[i][0] = tws[str(i)][0]
            self.time_windows[i][1] = tws[str(i)][1]


    def read_specific_input(self, file_name):
        print(file_name)


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
        self.time_windows_size = int(time_windows_size)

        self.read_points(points_dict, n_points)
        self.distance_matrix = self.read_matrix(dist_mat)
        self.time_matrix = self.read_matrix(time_mat)
        self.read_pickups_and_deliveries(pds)
        self.read_demands(dem)
        self.read_services_times(serv_times)
        self.read_time_windows(tws)


    def get_reader_solver_attributes_relation(self):
        reader_solver_attributes_relation = {
            "points" : "points",
            "distance_matrix" : "distance_matrix",
            "time_matrix" : "time_matrix",
            "capacity" : "capacity",
            "demands" : "demands",
            "services_times" : "services_times",
            "time_windows" : "time_windows",
            "planning_horizon" : "planning_horizon",
            "time_windows_size" : "time_windows_size",
            "origin" : "origin_id",
            "pickups" : "pickups_ids",
            "deliveries" : "deliveries_ids"
        }

        return reader_solver_attributes_relation

