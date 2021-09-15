from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator


class InsertionOperatorPDPTW(InsertionOperator):
    def __init__(self):
        super().__init__("Insertion Operator for PDPTW")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.vertices = None
        self.time_matrix = None
        self.depot = None
        self.number_of_requests = None


    def try_to_insert(self, route, position, request, obj_func, constraints):
        return super().try_to_insert(
            route, 
            position, 
            request, 
            obj_func, 
            constraints
        )

    
    def get_child_class_route_feasible_insertions(
        self, 
        route, 
        request, 
        obj_func, 
        constraints
    ):
        if (route.empty()):
            new_route = self.try_to_insert(
                route,
                (0, 1), 
                request,
                obj_func,
                constraints 
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
                    obj_func, 
                    constraints
                )
                
                if (new_route is None):
                    continue

                feasible_positions.append((
                    (i, j),
                    new_route
                ))
        
        return feasible_positions


    def update_solution_requests_costs_after_insertion(
        self, 
        solution, 
        route, 
        position, 
        request, 
        obj_func
    ):
        route_order = route.requests_order()
        pick_pos, deli_pos = position
        pick_prev_pair = (-1, -1)
        if (pick_pos > 0):
            pick_prev_id = route_order[pick_pos-1]
            pick_prev_pair = (
                pick_prev_id,
                pick_prev_id + self.number_of_requests
            )
            if (pick_prev_id > self.number_of_requests):
                pick_prev_pair = (
                    pick_prev_id - self.number_of_requests,
                    pick_prev_id
                )
        
        deli_next_pair = (-1, -1)
        if (deli_pos < route.size()-1):
            deli_next_id = route_order[deli_pos+1]
            deli_next_pair = (
                deli_next_id,
                deli_next_id + self.number_of_requests
            )
            if (deli_next_id > self.number_of_requests):
                deli_next_pair = (
                    deli_next_id - self.number_of_requests,
                    deli_next_id
                )
        pick_next_pair = (-1, -1)
        deli_prev_pair = (-1, -1)
        if (pick_pos < deli_pos-1):
            pick_next_id = route_order[pick_pos+1]
            pick_next_pair = (
                pick_next_id,
                pick_next_id + self.number_of_requests
            )
            if (pick_next_id > self.number_of_requests):
                pick_next_pair = (
                    pick_next_id - self.number_of_requests,
                    pick_next_id
                )
            
            deli_prev_id = route_order[deli_pos-1]
            deli_prev_pair = (
                deli_prev_id,
                deli_prev_id + self.number_of_requests
            )
            if (deli_prev_id > self.number_of_requests):
                deli_prev_pair = (
                    deli_prev_id - self.number_of_requests,
                    deli_prev_id
                )
        
        pairs = (
            set([
                request,
                pick_prev_pair,
                deli_next_pair,
                pick_next_pair,
                deli_prev_pair
            ])
        )
        pairs.discard((-1, -1))

        dict_costs = {}
        for pair in pairs:
            pos_pair = route.index(pair)
            dict_costs[pair] = obj_func.get_request_cost_in_route(
                route,
                pos_pair,
                pair
            )
        
        for pair, cost in dict_costs.items():
            solution.set_request_cost(pair, cost)


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
        route_order = route.requests_order()
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
        route_order = route.requests_order()
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


    def get_attr_relation_reader_insert_op(self):
        rela_reader_heur = {
            "vertices" : "vertices",
            "number_of_requests" : "number_of_requests",
            "time_matrix" : "time_matrix",
            "depot" : "depot"
        }
        return rela_reader_heur




