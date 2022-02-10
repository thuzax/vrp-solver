from src.objective_functions import ObjVehiclePDPTW

class ObjVehicleDPDPTW(ObjVehiclePDPTW):

    def __init__(self):
        super().__init__()

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.big_m = None
        self.requests = None

    def get_solution_cost(self, solution):
        all_routes_cost = len(solution.routes)
        not_fulfilled_requests = len(set(self.requests) - solution.requests())
        
        total_cost = all_routes_cost + (not_fulfilled_requests * self.big_m)

        return total_cost


    @staticmethod
    def get_attr_relation_reader_func():
        solver_func_attr_rela = {
            "distance_matrix" : "distance_matrix",
            "depot" : "depot",
            "requests" : "requests"
        }
        return solver_func_attr_rela