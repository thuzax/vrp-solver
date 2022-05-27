
import copy
import random
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
import numpy
from src.solution_methods.SolutionMethod import SolutionMethod


class KRegret(SolutionMethod):

    def __init__(self):
        super().__init__("KRegret")
    
    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.non_insertion_cost = None
        self.use_modification = None
        
        self.k = None

    def get_m_best_routes(self, routes):
        m = self.k
        if (not self.use_modification or m == 1):
            return routes
        
        routes_costs_arr = numpy.array([
            route.cost()
            for route in routes
        ])

        best_posistions = numpy.argpartition(routes_costs_arr, m)[:m]
        best_routes = []
        for i in best_posistions:
            best_routes.append(routes[i])

        return best_routes


    def get_requests_best_feasible_insertions(self, requests, routes_sol):
        requests_feasible_insertions = {}
        routes = self.get_m_best_routes(routes_sol)
        for request in requests:
            feasible_insertions = []
            for route in routes:
                best_insertion = (
                    InsertionOperator().get_best_insertion_in_route(
                        route,
                        request,
                        self.obj_func,
                        self.constraints
                    )
                )
                if (any(best_insertion)):
                    feasible_insertions.append(best_insertion)
                    continue
                
                feasible_insertions.append(
                    (None, None, self.non_insertion_cost)
                )

            requests_feasible_insertions[request] = feasible_insertions

        
        return requests_feasible_insertions

    def get_insertions_and_regret_value(self, requests, feasible_insertions):
        insertions_and_regret_values = {}
        for request in requests:
            request_feasible_insertions = feasible_insertions[request]
            insert_costs_arr = numpy.array(
                [
                    insert_cost
                    for pos, route, insert_cost in request_feasible_insertions
                ]
            )
            if (self.k > len(insert_costs_arr)):
                k_best_insertions_pos = (
                    numpy.argpartition(insert_costs_arr, self.k)[:self.k]
                )

                k_feasible_insertions = [
                    request_feasible_insertions[i]
                    for i in k_best_insertions_pos
                ]

            else:
                k_best_insertions_pos = [i for i in range(self.k)]
                k_feasible_insertions = request_feasible_insertions
            
            min_insertion_pos = numpy.argmin(insert_costs_arr)
            
            if (not all(request_feasible_insertions[min_insertion_pos])):
                continue
            
            if (min_insertion_pos not in k_best_insertions_pos):
                i = 0
                found = False
                while (i < len(k_best_insertions_pos) and not found):
                    pos = k_best_insertions_pos[i]
                    if (
                        insert_costs_arr[pos] 
                        != insert_costs_arr[min_insertion_pos]
                    ):
                        i += 1
                        continue
                    found = True
                    min_insertion_pos = pos
                    

            regret_value = 0
            pos_min, route_min, insert_cost_min = (
                request_feasible_insertions[min_insertion_pos]
            )
            for i in range(self.k):
                pos_i, route_i, insert_cost_i = k_feasible_insertions[i]

                regret_value += (
                    insert_cost_i - insert_cost_min
                )
            insertions_and_regret_values[request] = (
                request_feasible_insertions[min_insertion_pos],
                regret_value
            )
        
        return insertions_and_regret_values


    def solve(self, solution, parameters):
        self.k = parameters["k"]
        try:
            only_route_pos = parameters["route"]
        except:
            only_route_pos = None
        
        requests = copy.deepcopy(parameters["requests_set"])
        new_solution = solution.copy()

        could_insert = True
        i = 0

        while (could_insert and len(requests) > 0):
            if (only_route_pos is not None):
                routes = [new_solution.routes()[only_route_pos]]
            else:
                routes = new_solution.routes()

            feasible_insertions = self.get_requests_best_feasible_insertions(
                requests,
                routes
            )
            
            insertions_and_regret_values = self.get_insertions_and_regret_value(
                requests, 
                feasible_insertions
            )
            
            if (len(insertions_and_regret_values) == 0):
                could_insert = False
                continue
            
            request, items = max(
                insertions_and_regret_values.items(), 
                key=lambda x : x[1][1]
            )

            insertion, regret_value = insertions_and_regret_values[request]
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



            requests.discard(request)

        return new_solution


    def get_current_best_solution(self):
        return super().get_current_best_solution()

    def update_route_values(self, route, position, request):
        return super().update_route_values(route, position, request)

    def get_attr_relation_reader_heuristic(self):
        return super().get_attr_relation_reader_heuristic()