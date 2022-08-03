import copy
from src import file_log

from src.route_classes.RouteDPDPTW import RouteDPDPTW


class RouteDPDPTWHeterogeneousFleet(RouteDPDPTW):

    def __init__(self, fleet_type=None, *args, **kwargs):
        super().__init__("Route DPDPTWHeterogeneousFleet")
        if (self.fleet_type_set is None):
            self.fleet_type_set = fleet_type
        if (self.fleet_type_set is not None):
            self.calculate_route_id_value()

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fleet_type_set = None

    def can_attend(self, attendance_type):
        return (attendance_type in self.fleet_type_set)

    def calculate_route_id_value(self):
        list_types = list(self.fleet_type_set)
        list_types.sort()
        self.id_value = tuple(list_types + [-1] + self.vertices_order)


    def get_id_value_without_request(self, request):
        request = set(request)

        sep_pos = 0
        route_id = self.get_id_value()
        while (route_id[sep_pos] >= 0):
            sep_pos += 1
        
        id_without_request = tuple([
            route_id[i]
            for i in range(len(route_id))
            if (route_id[i] not in request) or (i <= sep_pos)
        ])

        # if (len(route_id)-len(request) > len(id_without_request)):
        #     for i in range(len(route_id)):
        #         print(route_id[i] not in request)
        #         print(i <= sep_pos)
        #         if (route_id[i] not in request) or (i <= sep_pos):
        #             print(route_id[i])
        #     print(request)
        return id_without_request


    def get_attendance_type(self):
        return self.fleet_type_set

    def copy_route_to(self, route_copy):
        super().copy_route_to(route_copy)
        route_copy.fleet_type_set = copy.deepcopy(self.fleet_type_set)


    def __str__(self):
        text = super().__str__()
        text += "ATT TYPE: " + str(self.fleet_type_set)
        return text