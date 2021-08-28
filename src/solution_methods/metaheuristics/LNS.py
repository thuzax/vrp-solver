
from src.solution_methods.SolutionMethod import SolutionMethod

from src.solution_methods.SolutionMethod import SolutionMethod

class LNS(SolutionMethod):
    

    def __init__(self):
        super().__init__("LNS")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()


    def solve(self, solution, parameters):
        super().solve()


    def update_solution_requests_costs(
        self, 
        solution, 
        route, 
        position, 
        request
    ):
        return super().update_solution_requests_costs(
            solution, 
            route, 
            position,
            request
        )


    def update_route_values(self, route, position, request):
        super().update_route_values(route, position, request)


    @staticmethod
    def get_attr_relation_reader_heuristic():
        rela_reader_heur = SolutionMethod.get_attr_relation_reader_heuristic()
        return rela_reader_heur