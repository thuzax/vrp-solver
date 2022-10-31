

from src.objective_functions import ObjFunctionPDPTW

class ObjVehiclePDPTW(ObjFunctionPDPTW):


    def __init__(self):
        self.distance_matrix = None
        self.depot = None
        super().__init__("Vehicle Objective")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def get_solution_cost(self, solution):
        total_cost = 0
        for route in solution.routes():
            if (route.empty()):
                continue
            total_cost += 1
        
        return total_cost


    @staticmethod
    def get_attr_relation_reader():
        solver_func_attr_rela = {
            "distance_matrix" : "distance_matrix",
            "depot" : "depot"
        }
        return solver_func_attr_rela


    