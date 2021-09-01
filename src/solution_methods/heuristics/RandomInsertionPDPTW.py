from src.solution_methods.heuristics.RandomInsertion import RandomInsertion


class RandomInsertionPDPTW(RandomInsertion):

    def __init__(self):
        super().__init__("RandomInsertion PDPTW")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.vertices = None
        self.time_matrix = None
        self.depot = None
        self.number_of_requests = None


    def get_route_feasible_insertions(self, route, request):
        if (route.empty()):
            new_route = self.try_to_insert(
                route,
                (0, 1), 
                request, 
            )

            if (new_route is None):
                return []
            
            return [
                (
                    (0, 1),
                    new_route
                )
            ]
        
        feasible_positions = []
        for i in range(route.size()+1):
            for j in range(i+1, route.size()+2):
                new_route = self.try_to_insert(
                    route, 
                    (i, j), 
                    request, 
                )
                
                if (new_route is None):
                    continue

                feasible_positions.append((
                    (i, j),
                    new_route
                ))
        return feasible_positions


    def update_route_values(self, route, position, request):
        pickup_position, delivery_position = position
        
        for i in range(pickup_position, route.size()):
            arrival_time = (
                self.calculate_arrival_time(route, i)
            )
            occupied_capacity = (
                self.calculate_demand_on_vertex(route, i)
            )

            route.arrival_times[i] = arrival_time
            route.capacity_occupations[i] = occupied_capacity


    def calculate_demand_on_vertex(self, route, position):
        route_order = route.get_order()
        vertex_id = route_order[position]

        if (position == 0):
            return self.vertices[vertex_id].demand
        
        previous_occ = route.capacity_occupations[position-1] 

        demand = (
            previous_occ
            + self.vertices[vertex_id].demand
        )

        return demand


    def calculate_arrival_time(self, route, position):
        route_order = route.get_order()
        vertex_id = route_order[position]
        
        if (position == 0):
            return self.time_matrix[self.depot][vertex_id]

        
        previous_id = route_order[position-1]
        
        previous_start_service = route.arrival_times[position-1]
        previous_tw = self.vertices[previous_id].time_window

        if (previous_start_service < previous_tw[0]):
            previous_start_service = previous_tw[0]

        previous_service_time = self.vertices[previous_id].service_time
        
        travel_time = self.time_matrix[previous_id][vertex_id]

        arrival_time = (
            previous_start_service 
            + previous_service_time 
            + travel_time
        )

        return arrival_time


    @staticmethod
    def get_attr_relation_reader_heuristic():
        rela_reader_heur = {
            "vertices" : "vertices",
            "number_of_requests" : "number_of_requests",
            "time_matrix" : "time_matrix",
            "depot" : "depot"
        }
        return rela_reader_heur

