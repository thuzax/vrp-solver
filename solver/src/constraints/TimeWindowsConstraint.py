from src import file_log
from src.constraints import Constraint


class TimeWindowsConstraint(Constraint):
    
    planning_limit = None
    time_matrix = None
    time_windows = None
    depot = None


    def __init__(self):
        super().__init__("Time Windwos Constraint")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.planning_limit = None
        self.time_matrix = None
        self.time_windows = None
        self.depot = None
        self.vertices = None


    def route_is_feasible(self, route, start_pos=0, end_pos=-1):
        if (route.empty()):
            return True
        
        route_order = route.requests_order()
        if (end_pos < 0):
            end_pos = len(route_order) + end_pos

        arr = []
        for i in range(start_pos, end_pos+1):
            vertex_arrival_time = route.arrival_times[i]
            
            vertex_id = route_order[i]
            end_tw = self.time_windows[vertex_id][1]
            arr.append(vertex_arrival_time > end_tw)

        if (any(arr)):
            return False
        
        if (end_pos < route.size()-1):
            return True
        
        # Planning Horizon
        last_delivery = route_order[end_pos]
        
        arrival_on_depot = (
            route.arrival_times[end_pos] 
            + self.vertices[last_delivery].service_time
            + self.time_matrix[last_delivery][self.depot]
        )

        end_tw_depot = self.time_windows[self.depot][1]
        if (arrival_on_depot > end_tw_depot):
            return False

        return True


    @staticmethod
    def get_attr_relation_reader():
        attr_relation = {
            "planning_horizon" : "planning_limit",
            "time_matrix" : "time_matrix",
            "time_windows" : "time_windows",
            "depot" : "depot",
            "vertices" : "vertices"
        }
        return attr_relation
