import json
import collections
from src.InstanceData import InstanceData

from src.get_subclasses import get_all_subclasses

class InstanceDataUR(InstanceData):

    def initialize_attrs(self, test_instance):
        self.test_instance = test_instance
        self.cost_matrix = None
        self.time_matrix = None
        self.capacity = None
        self.horizon = None
        self.tw_size = None
        self.depot = None
        self.fleet = None
        self.attendance_type = None
        self.fleet_size = None


    def read_data_from_instance(self):
        with open(self.test_instance, "r") as test_file:
            data_dict = json.loads(test_file.read())
        
        self.depot = data_dict["depot"]
        self.depot_point = data_dict["points"][str(self.depot)]

        self.cost_matrix = self.read_matrix(data_dict["distance_matrix"])
        self.time_matrix = self.read_matrix(data_dict["time_matrix"])

        self.capacity = data_dict["capacity"]
        self.horizon = data_dict["planning_horizon"]
        self.tw_size = data_dict["time_windows_size"]
        self.fleet = data_dict["fleet"]
        self.fleet_size = sum([fleet_item[0] for fleet_item in self.fleet])
        self.attendance_type = data_dict["attendance_type"]


    def make_requests_data_dict(
        self, 
        all_requests, 
        orig_to_mapped, 
        non_attended_ids
    ):
        points = {}
        
        # semaphore.acquire()
        points[0] = InstanceData().get_depot_point()
        # semaphore.release()
        
        demands = {}
        services_times = {}
        time_windows_pd = {}
        attendance_type = {}
        pickups_and_deliveries = []
        for orig, mapped in orig_to_mapped.items():
            request = all_requests[orig]
            
            points[mapped[0]] = request["points"][0]
            points[mapped[1]] = request["points"][1]

            
            if (orig in non_attended_ids):
                pickups_and_deliveries.append(mapped)
            
            demands[mapped[0]] = request["demands"][0]
            demands[mapped[1]] = request["demands"][1]

            services_times[mapped[0]] = request["services_times"][0]
            services_times[mapped[1]] = request["services_times"][1]

            time_windows_pd[mapped[0]] = request["time_windows"][0]
            time_windows_pd[mapped[1]] = request["time_windows"][1]

            attendance_type[mapped[0]] = request["attendance_type"][0]
            attendance_type[mapped[1]] = request["attendance_type"][1]

        requests_data_dict = {}
        
        requests_data_dict["number_of_points"] = len(points)

        points = dict(collections.OrderedDict(sorted(points.items())))
        requests_data_dict["points"] = points

        demands = dict(collections.OrderedDict(sorted(demands.items())))
        requests_data_dict["demands"] = demands

        services_times = dict(
            collections.OrderedDict(sorted(services_times.items()))
        )
        requests_data_dict["services_times"] = services_times
        
        time_windows_pd = dict(
            collections.OrderedDict(sorted(time_windows_pd.items()))
        )
        requests_data_dict["time_windows_pd"] = time_windows_pd
        
        requests_data_dict["pickups_and_deliveries"] = pickups_and_deliveries


        requests_data_dict["attendance_type"] = dict(
            collections.OrderedDict(sorted(attendance_type.items()))
        )
        # raise Exception(str(attendance_type))

        return requests_data_dict



    def make_instance_data_dict(self):
        capacity = self.capacity
        depot = self.depot
        planning_horizon = self.horizon
        time_windows_size = self.tw_size
        fleet = self.fleet
        attendance_type = self.attendance_type

        instance_data = {}

        instance_data["capacity"] = capacity
        instance_data["depot"] = depot
        instance_data["planning_horizon"] = planning_horizon
        instance_data["time_windows_size"] = time_windows_size
        instance_data["fleet"] = fleet
        instance_data["attendance_type"] = attendance_type

        return instance_data

    def get_attendance_type(self, point):
        return self.attendance_type[point]
