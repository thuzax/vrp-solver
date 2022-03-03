from src.objective_functions import ObjFunctionPDPTW

class ObjDistancePDPTW(ObjFunctionPDPTW):

    def __init__(self):
        super().__init__("Distance Objective")


    def initialize_class_attributes(self):
        self.distance_matrix = None
        self.depot = None
        super().initialize_class_attributes()


    def get_solution_cost(self, solution):
        return self.get_routes_sum_cost(solution.routes())


    @staticmethod
    def get_attr_relation_reader_func():
        solver_func_attr_rela = {
            "distance_matrix" : "distance_matrix",
            "depot" : "depot"
        }
        return solver_func_attr_rela

    