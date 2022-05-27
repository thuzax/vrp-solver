from src.constraints import Constraint

class AttendAllRequests(Constraint):
    

    def __init__(self):
        super().__init__("Attend All Requests Constraint")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.all_requests = None


    def route_is_feasible(self, route, start_pos=0, end_pos=-1):
        return True    


    def solution_is_feasible(self, solution):
        for request in self.all_requests:
            if (request not in solution.requests()):
                return False

        return True


    @staticmethod
    def get_attr_relation_solver_constr():
        attr_relation = {
            "requests" : "all_requests"
        }
        return attr_relation
