from src.solution_methods.heuristics.KRegret import KRegret


class KRegretPDPTW(KRegret):

    def __init__(self):
        super().__init__("KRegret PDPTW")

        self.vertices = None
        self.time_matrix = None
        self.depot = None


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
            "time_matrix" : "time_matrix",
            "depot" : "depot"
        }
        return rela_reader_heur

