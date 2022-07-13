import os
import json

from .get_subclasses import get_all_subclasses
from .InstanceData import InstanceData


class CurrentSolution:
    instance = None
    def __new__(cls, *args, **kwargs):
        for subcls in get_all_subclasses(cls):
            if (subcls.instance is not None):
                return subcls.instance
        
        if (cls.instance is None):
            cls.instance = super(CurrentSolution, cls).__new__(
                cls, *args, **kwargs
            )
            cls.instance.initialize_attrs()
        
        return cls.instance

    def initialize_attrs(self):
        self.routes = {}
        self.routes_costs = {}
        self.cost = 0
        self.vehicles_positions = {}
        self.predicted_positions = {}

        for i in range(InstanceData().fleet_size):
            self.routes[i] = []
            self.routes_costs[i] = 0


    def reset_routes(self, routes, costs, new_solution):
        for route_id, route in routes.items():
            new_id = self.set_next_route(route)
            if (new_id == None):
                new_id = self.set_in_new_route(route)
            self.set_route_cost(new_id, costs[route_id])
        self.set_cost(new_solution["solution_cost"])


    def set_in_new_route(self, route):
        for r_pos in range(len(self.routes)):
            if (len(self.routes[r_pos]) == 0):
                self.routes[r_pos] = route
                return r_pos
        
        return None


    def routes_are_equivalent(self, route, r, r_pos):
        predicted_pos = self.predicted_positions[r_pos]

        if (predicted_pos == -1):
            return False
        if (predicted_pos >= len(route)):
            return False
        
        found_different = False
        i = 0
        while (not found_different and i < predicted_pos):
            found_different = (r[i] != route[i])
            i += 1
        
        if (found_different):
            return False
        
        return True
        


    def set_next_route(self, route):
        for r_pos, r in self.routes.items():
            if (not self.routes_are_equivalent(route, r, r_pos)):
                continue
            self.routes[r_pos] = route
            return r_pos
        
        return None



    def set_route_cost(self, route_id, cost):
        if (route_id is None):
            return
        self.routes_costs[route_id] = cost

    def set_cost(self, solution_cost):
        self.cost = solution_cost



    def get_vehicles_positions(self):
        return self.vehicles_positions
    
    def get_routes(self):
        return self.routes

    def calculate_end_exec_predicted_positions(self, routes, ts_size, ts_id):
        for vehicle, route in routes.items():

            if (len(route) == 0):
                self.predicted_positions[vehicle] = -1
                continue

            total_time = int(ts_size * ts_id)
            i = 0
            
            total_time -= InstanceData().get_travel_time(
                0, 
                route[i]
            )

            while (total_time > 0 and i < len(route)-1):
                travel_time = InstanceData().get_travel_time(
                    route[i], 
                    route[i+1]
                )
                total_time -= travel_time
                i += 1
            
            predicted_pos = i
            self.predicted_positions[vehicle] = predicted_pos

    def get_predicted_positions(self):
        return self.predicted_positions
            
    def write_solution(self, output_path, slice):
        # print(self.routes)
        # print(self.routes_costs)
        # print(self.cost)

        dict_sol = {}
        dict_sol["solution"] = {}
        dict_sol["solution"]["routes"] = self.routes
        dict_sol["solution"]["costs"] = self.routes_costs
        dict_sol["solution"]["solution_routes_cost"] = sum(
            [x for x in self.routes_costs.values()]
        )
        dict_sol["solution"]["solution_cost"] = self.cost

        
        input_name = os.path.basename(InstanceData().test_instance)
        out_name = input_name.split(".")[0]
        out_name += "_" + str(slice) + "_sol.json"
        out_file_name = os.path.join(output_path, out_name)

        json_text = json.dumps(dict_sol)
        with open(out_file_name, "w") as out_file:
            out_file.write(json_text)

        # print("SOLUTION WIRTTEN IN")
        # print(out_file_name)


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
                "start" : predicted_position
            })

        current_routes_data = {}
        current_routes_data["fixed"] = fixed
        
        return current_routes_data