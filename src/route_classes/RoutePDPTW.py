
from src.route_classes import Route

class RoutePDPTW(Route):

    planning_horizon = None
    time_windows_size = None

    def __init__(self):
        super().__init__("Route PDPTW")


    def insert(self, vertex):
        self.vertices_order.append(vertex)
        self.vertices_set.add(vertex)

    def remove(self, vertex):
        self.vertices_set.remove(vertex)
        self.vertices_order.remove(vertex)


    @staticmethod
    def get_attribute_relation_solver_route():
        solver_route_attr_rela = {
            "planning_horizon" : "planning_horizon",
            "time_windows_size" : "time_windows_size"
        }
        
        return solver_route_attr_rela