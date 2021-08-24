
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
    start_id = None
    end_id = None
    pickups = None
    deliveries = None
    number_of_requests = None
    requests = None

    has_origin = None

    def __init__(self):
        super().__init__("PDPTW json input file Reader")
    
    
    def read_points(self, points_dict, n_points, start_id=None):
        self.has_origin = (start_id is not None)
        points = []
        index_increment = 0

        if (not self.has_origin):
            index_increment = 1
        
        for i in range(n_points):
            points.append(points_dict[str(i + index_increment)])

        # if doesn't have a origini
        if (not self.has_origin):
            #  add fake depot
            self.points = numpy.array(
                [[None, None]] + points, 
                dtype=float
            )
            self.number_of_points = n_points + 1
            self.start_id = 0
            self.end_id = 0
        else:
            # otherwise consider start_id and end_id the point in position 0
            self.points = numpy.array(points, dtype=float)
            self.number_of_points = n_points
            self.start_id = start_id
        


    def read_matrix(self, matrix_dict):
        # matrix = numpy.zeros(
        #     shape=(self.number_of_points, self.number_of_points), 
        #     dtype=int
        # )


        matrix = [
            [
                0
                for i in range(self.number_of_points)
            ]
            for i in range(self.number_of_points)
        ]

        index_incr = 0
        if (not self.has_origin):
            index_incr = 1

        for i in range(index_incr, self.number_of_points):
            for j in range(index_incr, self.number_of_points):

                matrix[i][j] = int(matrix_dict[str(i)][str(j)])

        matrix = tuple(map(tuple, matrix))

        return matrix


    def read_pickups_and_deliveries(self, pds):
        self.number_of_requests = len(pds)
        # pickups = first half of points
        self.pickups = numpy.array(
            [i for i in range(1, len(pds)+1)], 
            dtype=int
        )

        # deliveries = second half of points
        self.deliveries = numpy.array(
            [i + 1 + len(pds) for i in range(len(pds))], 
            dtype=int
        )

        self.requests = tuple([
            (self.pickups[i], self.deliveries[i])
            for i in range(len(pds))
        ])

        self.pickups = tuple(self.pickups)
        self.deliveries = tuple(self.deliveries)


    def read_demands(self, dem):
        self.demands = numpy.zeros((len(self.points)), dtype=int)

        self.demands[self.start_id] = 0
        self.demands[self.end_id] = 0

        index_increment = 0
        if (not self.has_origin):
            index_increment = 1

        for i in range(index_increment, len(self.pickups)+index_increment):
            self.demands[i] = dem[str(i)]
            self.demands[i+self.number_of_requests] = -dem[str(i)]
        
        self.demands = tuple(self.demands)


    def read_services_times(self, serv_times):
        self.services_times = numpy.zeros(len(self.points), dtype=int)

        self.services_times[self.start_id] = 0
        self.services_times[self.end_id] = 0

        index_increment = 0
        if (not self.has_origin):
            index_increment = 1
        
        for i in range(index_increment, len(self.points)):
            self.services_times[i] = serv_times[str(i)]

        self.services_times = tuple(self.services_times)


    def read_time_windows(self, tws):
        
        self.time_windows = numpy.zeros(
            shape=(self.number_of_points, 2),
            dtype=int
        )

        self.time_windows[self.start_id][0] = 0
        self.time_windows[self.end_id][0] = 0

        self.time_windows[self.start_id][1] = self.planning_horizon
        self.time_windows[self.end_id][1] = self.planning_horizon

        if (not self.has_origin):
            index_increment = 1
        
        for i in range(index_increment, len(self.points)):
            self.time_windows[i][0] = tws[str(i)][0]
            self.time_windows[i][1] = tws[str(i)][1]

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
        self.time_windows_size = int(time_windows_size)

        self.read_points(points_dict, n_points)
        self.distance_matrix = self.read_matrix(dist_mat)
        self.time_matrix = self.read_matrix(time_mat)
        self.read_pickups_and_deliveries(pds)
        self.read_demands(dem)
        self.read_services_times(serv_times)
        self.read_time_windows(tws)

