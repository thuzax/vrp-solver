from src.constraints import Constraint

class AttendAllRequests(Constraint):
    

    def __init__(self):
        super().__init__("Attend All Requests Constraint")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.all_requests = None


    def route_is_feasible(self, route):
        return True    


    def solution_is_feasible(self, solution):
        if (len(self.all_requests) > len(solution.requests())):
            return False
        return True


    @staticmethod
    def get_attr_relation_solver_constr():
        attr_relation = {
            "requests" : "all_requests"
        }
        return attr_relation
