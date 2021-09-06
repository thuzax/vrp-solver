
import random
import math
from pprint import pprint

from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
from src.solution_methods.basic_operators.RemovalOperatorPDPTW import RemovalOperatorPDPTW
from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator
from src.solution_methods.local_searches.LocalSearch import LocalSearch

class AGES(LocalSearch):

    def __init__(self):
        super().__init__("AGES")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.perturb_probabilities = None

        self.stop_criteria = None

        self.number_of_perturbations = None

        self.max_number_of_perturbations = None

        self.max_ejections = None


    def solve(self, solution, parameters):
        best_solution = solution.copy()

        self.number_of_perturbations = 0

        while (not self.stop_criteria_fulfilled()):
            new_solution = best_solution.copy()
            
            route_pos = random.randint(0, len(new_solution.routes)-1)
            removed_route = new_solution.pop_route(route_pos)
            
            if (new_solution.number_of_routes() == 0):
                return best_solution

            requests_stack = [
                request 
                for request in removed_route.get_requests_set()
            ]
            
            penalities = {request : 1 for request in solution.requests()}


            new_solution = self.reinsert_requests(
                requests_stack, 
                new_solution,
                penalities
            )

            if (len(requests_stack) == 0):
                print(
                    "IMPROVED", 
                    new_solution.cost(), 
                    new_solution.routes_cost()
                )
                self.number_of_perturbations = 0
                best_solution = new_solution

        return best_solution



    def reinsert_requests(self, requests_stack, solution, penalities):
        new_solution = solution.copy()

        while (len(requests_stack) > 0 and not self.stop_criteria_fulfilled()):
            request = requests_stack.pop()

            routes = [route for route in new_solution.routes]
            
            feasible_position = self.get_random_feasible_insertion(
                request, 
                routes
            )

            if (feasible_position is not None):
                insert_pos, route_after = feasible_position
                r = new_solution.find_route_position_by_id(route_after.get_id())
                InsertionOperator().insert_request_in_solution(
                    new_solution,
                    request,
                    insert_pos,
                    route_after,
                    r,
                    self.obj_func
                )
            else:
                penalities[request] += 1
                new_solution = self.eject_and_insert(
                    request, 
                    new_solution, 
                    requests_stack, 
                    penalities
                )
                solution = self.perturb(new_solution)
                self.number_of_perturbations += 1
        
        return new_solution


    def get_random_feasible_insertion(self, request, routes):
        can_insert = False
        while (not can_insert and len(routes) > 0):
            random_route_pos = random.randint(0, len(routes)-1)
            r = routes.pop(random_route_pos)
            feasible_insertions = (
                InsertionOperator().get_route_feasible_insertions(
                    r,
                    request,
                    self.obj_func,
                    self.constraints
                )
            )

            if (len(feasible_insertions) <= 0):
                continue
            
            can_insert = True

        if (not can_insert):
            return None
        
        feasible_insertion = random.choice(feasible_insertions)
        return feasible_insertion


    def eject_and_insert(self, request, solution, requests_stack, penalities):
        new_solution = solution.copy()
        ejections_and_insertions = self.get_ejections_and_insertions(
            request,
            new_solution
        )

        if (len(ejections_and_insertions) == 0):
            requests_stack.append(request)
            return solution

        ejections = [
            ejection
            for ejection in ejections_and_insertions.keys()
        ]

        ej_penalities = self.calculate_ejection_penality(ejections, penalities)

        minimal_value = min(ej_penalities.items(), key=lambda x : x[1])[1]
        minimals_ejections = [
            ejection 
            for ejection, value in ej_penalities.items()
            if value == minimal_value
        ]

        if (len(minimals_ejections) > 0):
            ejection = random.choice(minimals_ejections[:1])
        
        for pair in ejection:
            requests_stack.append(pair)

            pair_route = new_solution.get_request_route(pair)
            pair_pos_in_route = pair_route.index(pair)
            new_route = RemovalOperator().try_to_remove(
                pair_route,
                pair,
                self.obj_func,
                self.constraints
            )

            new_solution = RemovalOperator().remove_request_from_solution(
                new_solution,
                pair,
                pair_pos_in_route,
                new_route,
                new_solution.find_route_position_by_id(pair_route.get_id()),
                self.obj_func
            )

        insert_position, new_route = random.choice(
            ejections_and_insertions[ejection]
        )

        new_solution = InsertionOperator().insert_request_in_solution(
            new_solution,
            request,
            insert_position,
            new_route,
            new_solution.find_route_position_by_id(new_route.get_id()),
            self.obj_func
        )

        return new_solution


    def calculate_ejection_penality(self, ejections, penalities):
        ejections_penalities = {}
        for ejection in ejections:
            ejection_total_penality = 0
            for pair in ejection:
                ejection_total_penality += penalities[pair]
            ejections_penalities[ejection] = ejection_total_penality

        return ejections_penalities


    def get_ejections_and_insertions(self, request, solution):
        feasible_insertions_found = False
        k = 1
        while (not feasible_insertions_found and k <= self.max_ejections):
            if (k > 1):
                print("K > 1")
                exit(0)
            ejection_sets = self.get_ejection_sets(solution, k)
            ejections_and_insertions = {}
            for ejection_set in ejection_sets:
                feasible_insertions = self.get_ejection_set_insertions(
                    solution,
                    ejection_set,
                    request
                )
                if (len(feasible_insertions) > 0):
                    ejections_and_insertions[ejection_set] = feasible_insertions
            
            if (len(ejections_and_insertions) > 0):
                feasible_insertions_found = True
            k += 1

        return ejections_and_insertions


    def get_ejection_set_insertions(self, solution, ejection_set, request):
        routes_where_removed = {}
        for element in ejection_set:
            route_without_ejection_set = None

            old_route = solution.get_request_route(element)
            r = routes_where_removed.get(old_route.get_id())
            
            if (r is not None):
                old_route = r
            
            route_without_ejection_set = RemovalOperator().try_to_remove(
                old_route,
                element,
                self.obj_func,
                self.constraints
            )

            routes_where_removed[old_route.get_id()] = (
                route_without_ejection_set
            )
        
        feasible_insertions = (
            InsertionOperator().get_all_feasible_insertions_from_routes(
                request,
                routes_where_removed.values(),
                self.obj_func,
                self.constraints
            )
        )

        return feasible_insertions



    def get_ejection_sets(self, solution, k):
        possibles_ejections = []
        for request in solution.requests():
            ejection_sets = self.get_request_ejection_sets(
                request, 
                solution.requests() - {request},
                k
            )
            possibles_ejections += ejection_sets
        
        for i in range(len(possibles_ejections)):
            possibles_ejections[i] = frozenset(possibles_ejections[i])
        
        possibles_ejections = list(set(possibles_ejections))

        return possibles_ejections


    def get_request_ejection_sets(self, request, other_requests, size):
        if (size == 0):
            return [set()]
        
        ejection_sets = []
        
        for other_request in other_requests:
            other_request_sets = self.get_request_ejection_sets(
                other_request, 
                other_requests - {other_request},
                size-1
            )

            for request_set in other_request_sets:
                request_set.add(request)
                ejection_sets.append(request_set)

        return ejection_sets

        

    def perturb(self, solution):
        keys = list(self.perturb_probabilities.keys())
        probabilities = [self.perturb_probabilities[key] for key in keys]
        weights = [p/sum(probabilities) for p in probabilities]

        perturb_name = random.choices(keys, weights=weights)[0]
        perturb_operator = self.local_operators[perturb_name]
        new_solution = perturb_operator.solve(solution, {})

        return new_solution


    def accept(self, new_solution):
        return self.acceptance_algorithm.accept(new_solution)


    def stop_criteria_fulfilled(self):
        if (self.stop_criteria == "max_perturbation"):
            if (
                self.number_of_perturbations 
                < self.max_number_of_perturbations
            ):
                return False
        return True


    def define_local_searches_operators(self, op_dict):
        return super().define_local_searches_operators(op_dict)
        


    def update_route_values(self, route, position, request):
        super().update_route_values(route, position, request)


    def get_attr_relation_reader_heuristic(self):
        rela_reader_heur = super().get_attr_relation_reader_heuristic()
        return rela_reader_heur