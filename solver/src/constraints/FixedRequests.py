
from src import file_log
from src.constraints import Constraint

class FixedRequests(Constraint):
    

    def __init__(self):
        super().__init__("Fixed Requests Constraint")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fixed_routes_dicts = None
        self.parcial_requests = None
        self.completed_requests = None


    def route_is_feasible(self, route, start_pos=0, end_pos=-1):
            
        for fixed_route_dict in self.fixed_routes_dicts:
            fixed_requests = fixed_route_dict["requests"]
                    
            has_a_fixed_request = False
            
            for request in fixed_requests:
                if (request in route):
                    has_a_fixed_request = True
                    break

            fixed_route = fixed_route_dict["route"]
            st_pos = fixed_route_dict["start"]

            if (has_a_fixed_request):
                if (route.size() <= st_pos):
                    return False

                vertices_order = route.requests_order()

                for i in range(st_pos+1):
                    if (vertices_order[i] != fixed_route[i]):
                        return False

        return True



    def started_requests_are_in_solution(self, solution):
        for request in self.parcial_requests:
            if (request not in solution.requests()):
                return False
        
        for request in self.completed_requests:
            if (request not in solution.requests()):
                return False
        
        return True


    def solution_is_feasible(self, solution):
        if (not self.started_requests_are_in_solution(solution)):
            return False
        
        for route in solution.routes():
            if (not self.route_is_feasible(route)):
                return False
        
        return True


    @staticmethod
    def get_attr_relation_reader_constr():
        attr_relation = {
            "fixed_routes_dict" : "fixed_routes_dicts",
            "parcial_requests" : "parcial_requests",
            "completed_requests" : "completed_requests"
        }
        return attr_relation
