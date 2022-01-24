from src.objective_functions import ObjDistancePDPTW

class ObjDistanceDPDPTW(ObjDistancePDPTW):

    def __init__(self):
        super().__init__()


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.pickups = None
        self.vertices = None


    def route_additional_route_cost_after_insertion(
        self, 
        route, 
        position, 
        request
    ):
        """Calculate the increasing cost of route. It is considered that the 'request' inserted in 'positions' were the last insertion on the route and that the cost were updated.\n
        -Parameters:\n
        route -> Route() object;\n
        positions -> tuple of positions where request was inserted (pickup_pos, delivery_pos);\n
        request -> inserted request;"""

        pick_pos, deli_pos = position
        pick, deli = request

        pick_next = route.get_next_vertex_of_position(pick_pos)
        deli_next = route.get_next_vertex_of_position(deli_pos)


        if (
            pick_next in self.pickups
            and self.vertices[pick_next].is_fixed() 
            and not(self.vertices[pick].is_fixed())
        ):
            return 9999999999999

        if (
            deli_next in self.pickups
            and self.vertices[deli_next].is_fixed() 
        ):
            return 9999999999999

        return self.get_request_cost_in_route(route, position, request)


    @staticmethod
    def get_attr_relation_reader_func():
        solver_func_attr_rela = {
            "distance_matrix" : "distance_matrix",
            "depot" : "depot",
            "vertices" : "vertices",
            "pickups" : "pickups"
        }
        return solver_func_attr_rela

    