from src.solution_methods.SolutionMethod import SolutionMethod
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
from src import file_log


class FirstInsertion(SolutionMethod):
    children_instances = {}

    def __init__(self):
        super().__init__("First Insertion")

    def initialize_class_attributes(self):
        return super().initialize_class_attributes()


    def solve(self, solution, parameters):
        requests = parameters["requests_set"]
        try:
            only_route_pos = parameters["route"]
        except:
            only_route_pos = None
        new_solution = solution.copy()

        inserted_requests = set()

        for request in requests:
            routes = None
            if (only_route_pos is not None):
                routes = [new_solution.routes()[only_route_pos]]
            else:
                routes = new_solution.routes()

            insertion = InsertionOperator().get_first_feasible_insertion(
                routes,
                request,
                self.obj_func,
                self.constraints,
            )

            if (all(insertion)):
                inserted_requests.add(request)
            else:
                continue

            position, new_route, insert_cost = insertion

            old_route_identifying = (
                InsertionOperator().get_route_id_value_before_inserted(
                    new_route,
                    request
                )
            )

            old_route_pos = (
                new_solution.find_route_position_by_identifying_value(
                    old_route_identifying
                )
            )

            InsertionOperator().insert_request_in_solution(
                new_solution,
                request,
                position,
                new_route,
                old_route_pos,
                self.obj_func
            )

        return new_solution

    def update_route_values(self, route, position, request):
        return super().update_route_values()
    
    
    def get_attr_relation_reader_heuristic(self):
        return super().get_attr_relation_reader_heuristic()

            
    def get_current_best_solution(self):
        return super().get_current_best_solution()