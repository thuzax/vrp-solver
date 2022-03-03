from src.constraints import Constraint

class FixedRequests(Constraint):
    

    def __init__(self):
        super().__init__("Fixed Requests Constraint")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.fixed_routes_dicts = None

    def route_is_feasible(self, route):
        
        for fixed_route_dict in self.fixed_routes_dicts:
            fixed_requests = fixed_route_dict["requests"]


            has_a_fixed_request = False
            does_not_have_one_fixed_request = False
            
            for request in fixed_requests:
                if (request in route):
                    has_a_fixed_request = True
                else:
                    does_not_have_one_fixed_request = True

            if (has_a_fixed_request and does_not_have_one_fixed_request):
                return False

            fixed_route = fixed_route_dict["route"]
            non_fixed_start = fixed_route_dict["start"]
            if (has_a_fixed_request):
                vertices_order = route.requests_order()

                for i in range(non_fixed_start):
                    if (vertices_order[i] != fixed_route[i]):
                        return False

        return True


    def solution_is_feasible(self, solution):
        for fixed_route_dict in self.fixed_routes_dicts:
            for request in fixed_route_dict["requests"]:
                if (request not in solution.requests()):
                    return False

        for route in solution.routes():
            if (not self.route_is_feasible(route)):
                return False
        
        return True


    @staticmethod
    def get_attr_relation_solver_constr():
        attr_relation = {
            "fixed_routes_dict" : "fixed_routes_dicts",
        }
        return attr_relation
