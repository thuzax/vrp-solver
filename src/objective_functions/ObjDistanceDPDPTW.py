from src.objective_functions import ObjDistancePDPTW

class ObjDistanceDPDPTW(ObjDistancePDPTW):

    def __init__(self):
        super().__init__()


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.pickups = None
        self.vertices = None


    @staticmethod
    def get_attr_relation_reader_func():
        solver_func_attr_rela = {
            "distance_matrix" : "distance_matrix",
            "depot" : "depot",
            "vertices" : "vertices",
            "pickups" : "pickups"
        }
        return solver_func_attr_rela

    