import copy
from src.route_classes.RoutePDPTW import RoutePDPTW


class RoutePDPTWHybridFleet(RoutePDPTW):

    def __init__(self, fleet_type=None, *args, **kwargs):
        super().__init__("Route PDPTWHybridFleet")
        if (self.fleet_type_set is None):
            self.fleet_type_set = fleet_type

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fleet_type_set = None

    def can_attend(self, attendance_type):
        return (attendance_type in self.fleet_type_set)


    def copy_route_to(self, route_copy):
        super().copy_route_to(route_copy)
        route_copy.fleet_type_set = copy.deepcopy(self.fleet_type_set)

    def __str__(self):
        text = super().__str__()
        text += "ATT TYPE: " + str(self.fleet_type_set)
        return text