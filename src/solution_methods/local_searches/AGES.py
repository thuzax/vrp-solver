
import random
import time

from src import file_log
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator
from src.solution_methods.local_searches.LocalSearch import LocalSearch

class AGES(LocalSearch):

    def __init__(self):
        super().__init__("AGES")


    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.number_of_perturb_moves = None


        self.stop_criteria = None
        self.max_number_of_perturbations = None
        self.max_ejections = None

        self.stop_parameters = None
        self.ejection_sets_cache = None


    def get_current_best_solution(self):
        return super().get_current_best_solution()


    def solve(self, solution, parameters):
        self.best_solution = solution.copy()

        self.stop_parameters = {}
        self.stop_parameters["begin_time"] = time.time()
        self.stop_parameters["it"] = 0
        self.stop_parameters["number_perturb"] = 0
        self.stop_parameters["time_last_it"] = time.time()
        self.stop_parameters["time_last_improv"] = 0
        improved = False

        self.ejection_sets_cache = {}
        can_improve = True

        while (not self.stop_criteria_fulfilled() and can_improve):
            new_solution = self.best_solution.copy()
            
            route_pos = random.randint(0, len(new_solution.routes())-1)
            removed_route = new_solution.pop_route(route_pos)
            
            if (new_solution.number_of_routes() == 0):
                can_improve = False
                continue

            requests_stack = [
                request 
                for request in removed_route.requests()
            ]
            
            penalities = {request : 1 for request in solution.requests()}


            new_solution = self.reinsert_requests(
                requests_stack, 
                new_solution,
                penalities
            )

            self.stop_parameters["it"] += 1
            self.stop_parameters["time_last_it"] = time.time()
            if (
                len(requests_stack) == 0 
                and self.solution_is_feasible(new_solution)
                and self.accept(new_solution)
            ):
                improved = True
                self.stop_parameters["time_last_improv"] = time.time()
                self.stop_parameters["number_perturb"] = 0
                self.best_solution = new_solution
                self.best_solution.set_objective_value(
                    self.obj_func.get_solution_cost(self.best_solution)
                )
        
        message = "AGES" + "\n"
        message += "IT: " + str(self.stop_parameters["it"]) + "\n"
        message += "Exec Time: "
        message += str(
            self.stop_parameters["time_last_it"] 
            - self.stop_parameters["begin_time"]
        )
        message += "\n"
        message += "Improved\n" if improved else ""
        file_log.add_solution_log(self.best_solution, message)

        return self.best_solution


    def reinsert_requests(self, requests_stack, solution, penalities):
        new_solution = solution.copy()

        while (len(requests_stack) > 0 and not self.stop_criteria_fulfilled()):
            request = requests_stack.pop()

            routes = [route for route in new_solution.routes()]
            
            feasible_position = self.get_random_feasible_insertion(
                request, 
                routes
            )

            if (feasible_position is not None):
                insert_pos, route_after, insert_cost = feasible_position
                

                old_route_identifying_value = (
                    InsertionOperator().get_route_id_value_before_inserted(
                        route_after,
                        request
                    )
                )

                r = new_solution.find_route_position_by_identifying_value(
                    old_route_identifying_value
                )

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
                self.stop_parameters["number_perturb"] += 1
        
        return new_solution


    def get_random_feasible_insertion(self, request, routes):
        feasible_insertions = (
            InsertionOperator().get_all_feasible_insertions_from_routes(
                request,
                routes,
                self.obj_func,
                self.constraints
            )
        )
        
        if (len(feasible_insertions) <= 0):
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
        
        for req in ejection:
            requests_stack.append(req)

            req_route_pos, req_route = new_solution.get_request_route(req)
            req_pos_in_route = req_route.index(req)
            new_route = RemovalOperator().try_to_remove(
                req_route,
                req,
                self.obj_func,
                self.constraints
            )

            new_solution = RemovalOperator().remove_request_from_solution(
                new_solution,
                req,
                req_pos_in_route,
                new_route,
                req_route_pos,
                self.obj_func
            )

        insert_position, new_route, insert_cost = random.choice(
            ejections_and_insertions[ejection]
        )
        old_route_identifying_value = (
            InsertionOperator().get_route_id_value_before_inserted(
                new_route,
                request
            )
        )

        new_route_pos = new_solution.find_route_position_by_identifying_value(
            old_route_identifying_value
        )
        
        new_solution = InsertionOperator().insert_request_in_solution(
            new_solution,
            request,
            insert_position,
            new_route,
            new_route_pos,
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

            old_route_pos, old_route = solution.get_request_route(element)
            r = routes_where_removed.get(old_route.get_id_value())
            
            if (r is not None):
                old_route = r
            
            route_without_ejection_set = RemovalOperator().try_to_remove(
                old_route,
                element,
                self.obj_func,
                self.constraints
            )
            if (route_without_ejection_set is not None):
                routes_where_removed[old_route.get_id_value()] = (
                    route_without_ejection_set
                )
        # print(request)
        # print(routes_where_removed)
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
            ejection_sets = self.ejection_sets_cache.get(request)
            if (ejection_sets is None):
                ejection_sets = self.get_request_ejection_sets(
                    request, 
                    solution.requests() - {request},
                    k
                )
                self.ejection_sets_cache[request] = ejection_sets
            
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
        solution = self.local_operators["OriginalPerturbation"].solve(
            solution,
            {"n_perturb" : self.number_of_perturb_moves}
        )


    def stop_criteria_fulfilled(self):
        if (self.stop_criteria == "max_perturbation"):
            if (
                self.stop_parameters["number_perturb"] 
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