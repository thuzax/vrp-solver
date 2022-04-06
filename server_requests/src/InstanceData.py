import json

from src.get_subclasses import get_all_subclasses

class InstanceData:
    instance = None
    def __new__(cls, test_instance=None, *args, **kwargs):
        for subcls in get_all_subclasses(cls):
            if (subcls.instance is not None):
                return subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(InstanceData, cls).__new__(
                cls, *args, **kwargs
            )
            cls.instance.initialize_attrs(test_instance)
        
        return cls.instance
        

    def initialize_attrs(self, test_instance):
        self.test_instance = test_instance
        self.cost_matrix = None
        self.time_matrix = None
        self.capacity = None
        self.horizon = None
        self.tw_size = None
        self.depot = None


    def read_matrix(self, matrix_dict):
        matrix = [
            [
                0
                for i in range(len(matrix_dict))
            ]
            for i in range(len(matrix_dict))
        ]
        
        for i in range(len(matrix_dict)):
            for j in range(len(matrix_dict)):
                matrix[i][j] = int(matrix_dict[str(i)][str(j)])

        return matrix


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

    
    def get_travel_time(self, i, j):
        return self.time_matrix[i][j]

    def get_travel_cost(self, i, j):
        return self.cost_matrix[i][j]

    def get_depot_point(self):
        return self.depot_point