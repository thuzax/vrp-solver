import os
import json

from .CurrentSolution import CurrentSolution
from .InstanceData import InstanceData
from .InstanceDataUR import InstanceDataUR


class CurrentSolutionUR(CurrentSolution):
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
        self.routes_types = {}
        self.routes_att_types = {}
        self.routes_costs = {}
        self.cost = 0
        self.vehicles_positions = {}
        self.predicted_positions = {}

        for f_type, fleet in enumerate(InstanceData().fleet):
            fleet_size = fleet[0]
            fleet_att_types = fleet[1]
            fleet_type = f_type
            

            for i in range(fleet_size):
                self.routes[i] = []
                self.routes_costs[i] = 0
                self.routes_att_types[i] = fleet_att_types
                self.routes_types[i] = fleet_type

    def make_current_routes_data(
        self,
        routes, 
        predicted_positions, 
        orig_to_mapped_pick, 
        orig_to_mapped_deli
    ):
        fixed = []
        for vehicle, route in routes.items():
            predicted_position = predicted_positions[vehicle]
            route_mapped = []
            for vertex_id in route:
                if (vertex_id in orig_to_mapped_pick):
                    route_mapped.append(orig_to_mapped_pick[vertex_id])
                elif (vertex_id in orig_to_mapped_deli):
                    route_mapped.append(orig_to_mapped_deli[vertex_id])
            
            fixed.append({
                "route" : route_mapped,
                "fleet_type" : self.routes_types[vehicle],
                "start" : predicted_position
            })

        current_routes_data = {}
        current_routes_data["fixed"] = fixed
        
        return current_routes_data
            

    def set_next_route(self, route):
        for i, old_route in self.routes.items():
            if (not self.new_route_has_same_type(route, i)):
                continue
            if (not self.routes_are_equivalent(route, old_route, i)):
                continue
            
            self.routes[i] = route
            return i

        return None
        
    def new_route_has_same_type(self, route, old_route_pos):
        old_route_type = self.routes_att_types[old_route_pos]
        for point in route:
            point_type = InstanceDataUR().get_attendance_type(str(point))
            if (point_type not in old_route_type):
                return False
        return True



    def set_in_new_route(self, route):
        for r_pos in range(len(self.routes)):
            if (not self.new_route_has_same_type(route, r_pos)):
                continue

            if (len(self.routes[r_pos]) == 0):
                self.routes[r_pos] = route
                return r_pos
        
        return None