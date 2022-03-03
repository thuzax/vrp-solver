from src.solution_methods.acceptance_heuristics.AcceptanceHeuristic import AcceptanceHeuristic


class AcceptAll(AcceptanceHeuristic):

    def __init__(self):
        super().__init__("Accept All Solutions")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()

    def accept(self, new_solution, obj_func=None, parameters=None):
        return True

    def get_attr_relation_reader_accept_heuri(self):
        return {}