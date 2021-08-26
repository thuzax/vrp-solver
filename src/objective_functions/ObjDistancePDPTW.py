from src.objective_functions import ObjFunction

class ObjDistancePDPTW(ObjFunction):
    distance_matrix = None
    depot = None

    def __init__(self):
        super().__init__("Distance Objective")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def get_route_cost(self, route):
        route_order = route.get_order()
        
        route_cost = 0
        previous = self.depot
        for vertex in route_order:
            route_cost += self.distance_matrix[previous][vertex]
            previous = vertex

        route_cost += self.distance_matrix[previous][self.depot]

        return route_cost


    def get_solution_cost(self, solution):
        total_cost = 0
        for route in solution:
            total_cost += self.get_route_cost(route)

        return total_cost


    def route_additional_cost_after_insertion(self, route, positions, request):
        """Calculate the increasing cost of route. It is considered that the 'request' inserted in 'positions' were the last insertion on the route and that the cost were updated.\n
        -Parameters:\n
        route -> Route() object;\n
        positions -> tuple of positions where request was inserted (pickup_pos, delivery_pos);\n
        request -> inserted request;"""


        pick_pos, deli_pos = positions
        pickup, delivery = request

        # Calulate increasing distance for pickup
        pick_previous = route.get_previous_vertex_of_position(pick_pos)
        pick_next = route.get_next_vertex_of_position(pick_pos)
        if (pick_previous is None):
            dist_pick_to_previous = self.distance_matrix[self.depot][pickup]
        else:
            dist_pick_to_previous = self.distance_matrix[pick_previous][pickup]

        # Does not verify if it's None because delivery is allaways after pickup
        dist_pick_to_next = self.distance_matrix[pickup][pick_next]

        # Calculate increasing distance for delivery
        deli_previous = route.get_previous_vertex_of_position(deli_pos)
        deli_next = route.get_next_vertex_of_position(deli_pos)
        if (deli_next is None):
            dist_deli_to_next = self.distance_matrix[delivery][self.depot]
        else:
            dist_deli_to_next = self.distance_matrix[delivery][deli_next]
        # Does not verify if it's None because pickup is allaways before delivery
        dist_deli_to_previous = self.distance_matrix[deli_previous][delivery]

        # Increasing cost in any route
        ## pick_prv -> pick -> ... -> deli -> deli_nxt
        ## Does not add the cost of travel deli_prv -> deli yet,
        ## because if a sequencial insertion will add twice
        cost = 0
        cost += (
            + dist_pick_to_previous
            + dist_pick_to_next
            + dist_deli_to_next
        )

        # If pickup and delivery are sequential
        ## pick_prv -> pick ->  deli -> deli_nxt
        if (pick_pos == (deli_pos - 1)):
            # If it was the first insertion
            if (pick_previous is None and deli_next is None):
                dist_prv_nxt = self.distance_matrix[self.depot][self.depot]
            # If pickup was inserted in position 0
            elif (pick_previous is None):
                dist_prv_nxt = self.distance_matrix[self.depot][deli_next]
            # If delivery was inserted in last position
            elif (deli_next is None):
                dist_prv_nxt = self.distance_matrix[pick_previous][self.depot]
            # If insertion is in intern positions
            else:
                dist_prv_nxt = self.distance_matrix[pick_previous][deli_next]
            
            # Subtract the cost only once
            cost -= dist_prv_nxt
            return cost

        # if pickup and delivery are not sequential
        ## pick_prv -> pick -> pick_nxt -> ... -> deli_prv -> deli -> deli_nxt
        # Add the cost deli_previous -> delivery
        cost += dist_deli_to_previous
        
        # if pickup was inserted in position 0
        if (pick_previous is None):
            dist_pick_prv_nxt = self.distance_matrix[self.depot][pick_next]
        # if pickup was inserted in another position
        else:
            dist_pick_prv_nxt = self.distance_matrix[pick_previous][pick_next]

        # if delivery was inserted in last position
        if (deli_next is None):
            dist_deli_prv_nxt = self.distance_matrix[deli_previous][self.depot]
        # if delivery was inserted in another position
        else:
            dist_deli_prv_nxt = self.distance_matrix[deli_previous][deli_next]
        
        # subtract the distances from previous to next of pick and deli
        cost += (
            - dist_pick_prv_nxt
            - dist_deli_prv_nxt
        )

        return cost


    def route_reduced_cost_after_insertion(self, route, positions, request):
        """Calculate the deacresing cost of route. It is considered that the 'request' inserted in 'positions' were the last insertion on the route and that the cost were updated.\n
        -Parameters:\n
        route -> Route() object;\n
        positions -> position(s) of insertion;\n
        request -> request inserted"""
        if (route.empty()):
            return 0

        pick_pos, deli_pos = positions
        pickup, delivery = request

        # Calulate increasing distance for pickup
        pick_previous = route.get_previous_vertex_of_position(pick_pos)
        pick_next = route.get_next_vertex_of_position(pick_pos)
        if (pick_previous is None):
            dist_pick_to_previous = self.distance_matrix[self.depot][pickup]
        else:
            dist_pick_to_previous = self.distance_matrix[pick_previous][pickup]
        # Does not verify if it's None because delivery is allaways after pickup
        dist_pick_to_next = self.distance_matrix[pickup][pick_next]

        # Calculate increasing distance for delivery
        deli_previous = route.get_previous_vertex_of_position(deli_pos)
        deli_next = route.get_next_vertex_of_position(deli_pos)
        if (deli_next is None):
            dist_deli_to_next = self.distance_matrix[delivery][self.depot]
        else:
            dist_deli_to_next = self.distance_matrix[delivery][deli_next]
        # Does not verify if it's None because pickup is allaways before delivery
        dist_deli_to_previous = self.distance_matrix[deli_previous][delivery]

        # Increasing cost in any route
        ## pick_prv -> pick -> ... -> deli -> deli_nxt
        ## Does not add the cost of travel deli_prv -> deli yet,
        ## because if a sequencial insertion will add twice
        cost = 0
        cost += (
            - dist_pick_to_previous
            - dist_pick_to_next
            - dist_deli_to_next
        )

        # If pickup and delivery are sequential
        ## pick_prv -> pick ->  deli -> deli_nxt
        if (pick_pos == (deli_pos - 1)):
            # If it was the first insertion
            if (pick_previous is None and deli_next is None):
                dist_prv_nxt = self.distance_matrix[self.depot][self.depot]
            # If pickup was inserted in position 0
            elif (pick_previous is None):
                dist_prv_nxt = self.distance_matrix[self.depot][deli_next]
            # If delivery was inserted in last position
            elif (deli_next is None):
                dist_prv_nxt = self.distance_matrix[pick_previous][self.depot]
            # If insertion is in intern positions
            else:
                dist_prv_nxt = self.distance_matrix[pick_previous][deli_next]
            
            # Subtract the cost only once
            cost -= dist_prv_nxt
            return cost

        # if pickup and delivery are not sequential
        ## pick_prv -> pick -> pick_nxt -> ... -> deli_prv -> deli -> deli_nxt
        # Add the cost deli_previous -> delivery
        cost -= dist_deli_to_previous
        
        # if pickup was inserted in position 0
        if (pick_previous is None):
            dist_pick_prv_nxt = self.distance_matrix[self.depot][pick_next]
        # if pickup was inserted in another position
        else:
            dist_pick_prv_nxt = self.distance_matrix[pick_previous][pick_next]

        # if delivery was inserted in last position
        if (deli_next is None):
            dist_deli_prv_nxt = self.distance_matrix[deli_previous][self.depot]
        # if delivery was inserted in another position
        else:
            dist_deli_prv_nxt = self.distance_matrix[deli_previous][deli_next]
        
        # subtract the distances from previous to next of pick and deli
        cost += (
            + dist_pick_prv_nxt
            + dist_deli_prv_nxt
        )

        return cost


    @staticmethod
    def route_is_better(route_1, route_2):
        if (route_1 is None):
            return False
        
        if (route_2 is None):
            return True

        if (route_1.cost() > route_2.cost()):
            return False
        
        return True


    @staticmethod
    def get_attr_relation_reader_func():
        solver_func_attr_rela = {
            "distance_matrix" : "distance_matrix",
            "depot" : "depot"
        }
        return solver_func_attr_rela

    