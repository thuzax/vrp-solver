from src.solution_methods.basic_operators.InsertionOperatorPDPTW import InsertionOperatorPDPTW


class InsertionOperatorDPDPTW(InsertionOperatorPDPTW):
    def __init__(self):
        super().__init__("Insertion Operator for DPDPTW")

    def check_feasibility(self, route, constraints):
        start_pos = route.get_start_position()
        for constraint in constraints:
            if (not constraint.route_is_feasible(route, start_pos=start_pos)):
                return False
            
        return True