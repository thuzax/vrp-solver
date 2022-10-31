from src.constraints import Constraint

class HomogeneousCapacityConstraint(Constraint):

    def __init__(self):
        super().__init__("Homogenous Capacity Constraint")
            

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.vertices = None
        self.max_capacity = None
        self.demands = None


    def route_is_feasible(self, route, start_pos=0, end_pos=-1):
        if (route.empty()):
            return True
        
        route_order = route.requests_order()
        if (end_pos < 0):
            end_pos = len(route_order) + end_pos

        for i in range(start_pos, end_pos+1):
            if (route.capacity_occupations[i] > self.max_capacity):
                return False
        
        return True
    
    def solution_is_feasible(self, solution):
        return super().solution_is_feasible(solution)

    @staticmethod
    def get_attr_relation_reader():
        attr_relation = {
            "vertices" : "vertices",
            "capacity" : "max_capacity"
        }
        return attr_relation


    def set_attribute(self, name, value):
        super().set_attribute(name, value)

