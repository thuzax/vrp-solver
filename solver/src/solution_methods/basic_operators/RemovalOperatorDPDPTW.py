from src.solution_methods.basic_operators.RemovalOperatorPDPTW import RemovalOperatorPDPTW

class RemovalOperatorDPDPTW(RemovalOperatorPDPTW):
    
    def __init__(self):
        super().__init__("Removal Operator for DPDPTW")


    def check_feasibility(self, route, constraints):
        start_pos = route.get_start_position()
        for constraint in constraints:
            if (not constraint.route_is_feasible(route, start_pos=start_pos)):
                return False
            
        return True