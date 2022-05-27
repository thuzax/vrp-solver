import copy

from src.route_classes.RoutePDPTW import RoutePDPTW


class RouteDPDPTW(RoutePDPTW):

    def __init__(self, *args, **kwargs):
        super().__init__("Route DPDPTW")
        if (self.start_position is None):
            self.start_position = 0

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.start_position = None


    def set_start_position(self, start_position):
        if (self.start_position is None):
            self.start_position = start_position

    
    def get_start_position(self):

        return self.start_position

    def copy_route_to(self, route_copy):
        super().copy_route_to(route_copy)
        route_copy.start_position = self.start_position


    def __str__(self):
        text = super().__str__()
        text += "START POSITION: " + str(self.start_position) + "\n"
        return text