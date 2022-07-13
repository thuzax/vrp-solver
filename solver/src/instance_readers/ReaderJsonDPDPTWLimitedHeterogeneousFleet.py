
import json

from src import file_log

from src.instance_readers.ReaderJsonDPDPTW import ReaderJsonDPDPTW


class ReaderJsonDPDPTWLimitedHeterogeneousFleet(ReaderJsonDPDPTW):

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fleet = None
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

            fleet = input_dict["fleet"]
            attendance_type = input_dict["attendance_type"]

        self.capacity = int(cap)
        self.planning_horizon = int(planning_horizon)

        if (time_windows_size is not None):
            self.time_windows_size = int(time_windows_size)

        self.read_points(points_dict, n_points)
        self.distance_matrix = self.read_matrix(dist_mat)
        self.time_matrix = self.read_matrix(time_mat)

        self.fleet, self.fleet_size = self.read_fleet(fleet)
        self.attendance_type = self.read_attendance_type(attendance_type)

        self.read_pickups_and_deliveries(pds)
        self.fixed_routes_dict = self.read_fixed(fixed_requests)

        self.read_demands(dem)
        self.read_services_times(serv_times)
        self.read_time_windows(tws)

        

    def read_fleet(self, fleet):
        fleet_data = {}
        total_fleet_size = 0
        for i, fleet_element in enumerate(fleet):
            fleet_data[i] = {}
            fleet_data[i]["size"] = fleet_element[0]
            fleet_data[i]["types"] = set(fleet_element[1])
            total_fleet_size += fleet_data[i]["size"]
        return (fleet_data, total_fleet_size)


    def read_attendance_type(self, attendance_type):
        att_type = {}
        for key, value in attendance_type.items():
            att_type[int(key)] = value
        
        return att_type

    def create_specific_vertices(self):
        super().create_specific_vertices()
        for vertex_id, attendance_type in self.attendance_type.items():
            self.vertices_dict[vertex_id].set_attendance_type(attendance_type)