from src.constraints import Constraint

class PickupDeliveryConstraint(Constraint):

    def __init__(self):
        super().__init__("Pickup and Delivery Constraint")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.pickups = None
        self.deliveries = None
        self.number_of_requests = None
        self.vertices = None


    def route_is_feasible(self, route, start_pos=0, end_pos=-1):
        if (route.empty()):
            return True
            
        route_order = route.requests_order()

        if (end_pos < 0):
            end_pos = route.size() + end_pos

        route_order = route_order[start_pos:end_pos+1]

        set_pickups = self.pickups
        set_deliveries = self.deliveries
        
        pickups_found = {}
        deliveries_found = {}


        for vertex in route_order:
            if (vertex in set_pickups):
                pickups_found[vertex] = True
            
            if (vertex in set_deliveries):
                deliveries_found[vertex] = True
                pair_pickup = vertex - self.number_of_requests
                
                # if pickup did not come before delivery
                pickup_was_found = pickups_found.get(pair_pickup)
                if (not pickup_was_found):
                    return False
        
        for vertex in pickups_found.keys():
            pair_delivery = vertex + self.number_of_requests
            
            delivery_was_found = deliveries_found.get(pair_delivery)
            if (delivery_was_found):
                return True
        
        return False


    

    @staticmethod
    def get_attr_relation_reader():
        attr_relation = {
            "pickups" : "pickups",
            "deliveries" : "deliveries",
            "number_of_requests" : "number_of_requests",
        }
        return attr_relation
