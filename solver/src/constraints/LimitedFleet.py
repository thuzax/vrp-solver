from src.constraints import Constraint

class LimitedFleet(Constraint):
    

    def __init__(self):
        super().__init__("Limited Fleet Constraint")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fleet_size = None


    def route_is_feasible(self, route):
        return True


    def solution_is_feasible(self, solution):
        if (len(solution.routes()) > self.fleet_size):
            return False

        return True


    @staticmethod
    def get_attr_relation_solver_constr():
        attr_relation = {
            "fleet_size" : "fleet_size"
        }
        return attr_relation
