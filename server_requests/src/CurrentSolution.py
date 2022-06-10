
from .InstanceData import InstanceData


class CurrentSolution:
    instance = None
    def __new__(cls, *args, **kwargs):
        if (cls.instance is None):
            cls.instance = super(CurrentSolution, cls).__new__(
                cls, *args, **kwargs
            )
            cls.instance.initialize_attrs()
        
        return cls.instance

    def initialize_attrs(self):
        self.routes = {}
        # self.routes = {}
        self.vehicles_positions = {}
        self.predicted_positions = {}

    def get_vehicles_positions(self):
        return self.vehicles_positions
    
    def get_routes(self):
        return self.routes

    def calculate_end_exec_predicted_positions(self, routes, ts_size, ts_id):
        
        for vehicle, route in routes.items():
            total_time = int((ts_size * ts_id)/60)
            i = 0
            print("CALCULATING")
            while (total_time > 0 and i < len(route)):
                travel_time = InstanceData().get_travel_time(i, i+1)
                print(i, i+1, travel_time, total_time)
                total_time -= travel_time
                i += 1
            predicted_pos = i + 1
            self.predicted_positions[vehicle] = predicted_pos
        

    def get_predicted_positions(self):
        print(self.predicted_positions)
        return self.predicted_positions
            