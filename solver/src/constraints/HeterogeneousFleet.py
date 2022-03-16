from src.constraints import Constraint


class HeterogeneousFleet(Constraint):

    def __init__(self):
        super().__init__("Heterogeneous Fleet Constraint")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.vertices = None

    def route_is_feasible(self, route):
        for request in route.requests():
            pick_vertex_id, deli_vertex_id = request
            pick_vertex = self.vertices[pick_vertex_id]
            deli_vertex = self.vertices[deli_vertex_id]

            pick_attendance = pick_vertex.get_attendance_type()
            deli_attendance = deli_vertex.get_attendance_type()
            if (
                not(
                    route.can_attend(pick_attendance)
                    and route.can_attend(deli_attendance)
                )
            ):
                return False

        return True

    def solution_is_feasible(self, solution):
        return True

    @staticmethod
    def get_attr_relation_solver_constr():
        attr_relation = {
            "vertices": "vertices"
        }
        return attr_relation
