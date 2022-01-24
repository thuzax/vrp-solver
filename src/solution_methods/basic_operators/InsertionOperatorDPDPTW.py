from src.solution_methods.basic_operators.InsertionOperatorPDPTW import InsertionOperatorPDPTW


class InsertionOperatorDPDPTW(InsertionOperatorPDPTW):
    def __init__(self):
        super().__init__()


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def try_to_insert(
        self, 
        route, 
        position, 
        request, 
        obj_func, 
        constraints,
        is_fixed=False
    ):
        copy_route = route.copy()
        params = {}
        params["is_fixed"] = is_fixed
        copy_route.insert(position, request, params)

        self.update_route_values(copy_route, position, request)
        additional_cost = obj_func.route_additional_route_cost_after_insertion(
            copy_route,
            position, 
            request
        )
        copy_route.route_cost += (
            additional_cost
        )

        for constraint in constraints:
            if (not constraint.route_is_feasible(copy_route)):
                return None
        
        return copy_route
    