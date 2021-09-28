

import copy
from src import exceptions
from src import file_log
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
import time
from src.solution_check import solution_check
from src.solution_check import get_solution_check_complete_data
from src.solution_methods.local_searches.LocalSearch import LocalSearch


class SBMath(LocalSearch):

    def __init__(self):
        super().__init__("Sartori and Buriol 2020 Matheuristic")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        
        self.stop_criteria = None
        self.max_time = None
        self.max_time_without_improv = None
        self.max_it = None
        self.max_it_without_improv = None
        self.routes_diff_method = None

        self.number_of_perturb_moves = None


    def execute_operator(self, initial_solution, operator_name, parameters):
        copy_solution = initial_solution.copy()

        operator = self.local_operators[operator_name]
        new_solution = operator.solve(copy_solution, parameters)

        obj_value = self.obj_func.get_solution_cost(new_solution)
        new_solution.set_objective_value(obj_value)
        
        routes_costs = self.obj_func.get_routes_sum_cost(new_solution.routes)
        new_solution.set_routes_cost(routes_costs)

        new_best_found = self.obj_func.solution_is_better(
            self.local_operators[operator_name].get_current_best_solution(), 
            self.best_solution
        )
        if (new_best_found):
            self.best_solution = new_solution
            self.iteration_without_imp = 0

        return new_solution

    def add_routes_to_pool_diff_by_order(self, routes):
        start = time.time()
        if (len(self.routes_pool) == 0):
            for route in routes:
                key = route.get_id_value()
                self.routes_pool_dict[key] = route.copy()
            
            self.routes_pool = list(self.routes_pool_dict.values())

        for route in routes:
            key = route.get_id_value()
            if (key in self.routes_pool_dict):
                continue
            self.routes_pool_dict[key] = route.copy()

        self.routes_pool = list(self.routes_pool_dict.values())

        print("Time adding in pool:", time.time() - start)


    def add_routes_to_pool_diff_by_set(self, routes):
        start = time.time()
        if (len(self.routes_pool) == 0):
            for route in routes:
                key = frozenset(route.requests())
                self.routes_pool_dict[key] = route.copy()
            
            self.routes_pool = list(self.routes_pool_dict.values())

        for route in routes:
            key = frozenset(route.requests())
            if (key not in self.routes_pool_dict):
                self.routes_pool_dict[key] = route.copy()
                continue
            is_better = self.obj_func.route_is_better(
                route, 
                self.routes_pool_dict[key]
            )
            if (is_better):
                self.routes_pool_dict[key] = route

        self.routes_pool = list(self.routes_pool_dict.values())

        # print("Time adding in pool:", time.time() - start)


    def add_routes_to_pool(self, routes):
        if (self.routes_diff_method == "set"):
            self.add_routes_to_pool_diff_by_set(routes)
            return
        if (self.routes_diff_method == "order"):
            self.add_routes_to_pool_diff_by_order(routes)
            return
        
        raise exceptions.RoutesDiffMethodNotSpecified(self.name)


    def solve(self, initial_solution, parameters):
        solution = initial_solution.copy()
        
        all_requests = copy.deepcopy(parameters["requests_set"])

        self.begin_time = time.time()
        self.time_last_it = self.begin_time

        self.iteration = 0
        self.iteration_without_imp = 0


        self.routes_pool = []
        self.routes_pool_dict = {}
        
        self.best_solution = solution
        self.add_routes_to_pool(solution.routes)

        while (not self.stop_criteria_fulfilled()):
            self.iteration += 1
            # Incr
            self.iteration_without_imp += 1

            it_start = time.time()
            remaining_req = all_requests - solution.requests()
            parameters = {
                "remaining_requests" : remaining_req
            }
            start_op = time.time()
            new_solution = self.execute_operator(
                solution, 
                "AGES", 
                parameters
            )
            end_op = time.time()
            exec_time = end_op - start_op
            # self.print_solution_pos_operator_status(
            #     new_solution, 
            #     "AGES", 
            #     exec_time
            # )

            parameters = {
                "remaining_requests" : remaining_req
            }
            start_op = time.time()
            new_solution = self.execute_operator(
                new_solution, 
                "LNS", 
                parameters
            )

            end_op = time.time()
            exec_time = end_op - start_op
            # self.print_solution_pos_operator_status(
            #     new_solution, 
            #     "LNS", 
            #     exec_time
            # )

            self.add_routes_to_pool(solution.routes)
            InsertionOperator().clean_feasible_insertions_cache_with_exception(
                new_solution.routes
            )

            parameters = {
                "requests_set" : all_requests,
                "routes_pool" : self.routes_pool
            }
            start_op = time.time()
            sp_solution = self.execute_operator(
                new_solution, 
                "SetPartitionModel", 
                parameters
            )

            end_op = time.time()
            exec_time = end_op - start_op
            # self.print_solution_pos_operator_status(
            #     new_solution, 
            #     "SetPartitionModel", 
            #     exec_time
            # )
            
            acc_parameters = {
                "best_solution" : self.best_solution,
                "probability" : self.iteration_without_imp / self.iteration
            }
            
            if (self.accept(sp_solution, acc_parameters)):
                solution = sp_solution
            else:
                solution = new_solution

            parameters = {
                "n_perturb" : self.number_of_perturb_moves
            }
            start_op = time.time()
            sp_solution = self.execute_operator(
                new_solution, 
                "OriginalPerturbation", 
                parameters
            )
            message = "OriginalPerturbation"
            message += "\n"
            message += "Exec Time: " + str(time.time() - start_op)
            message += "\n"
            file_log.add_solution_log(new_solution, message)
            

            end_op = time.time()
            exec_time = end_op - start_op
            # self.print_solution_pos_operator_status(
            #     new_solution, 
            #     "OriginalPerturbation", 
            #     exec_time
            # )

            self.time_last_it = time.time()


            message = ""
            message += "SBMath" + "\n"
            message += "IT: " + str(self.iteration) + "\n"
            message += "ITs witout improving: " 
            message += str(self.iteration_without_imp) + "\n"
            message += "IT time: " + str(time.time() - it_start) + "\n"
            message += "Time since begin: "
            message += str(time.time() - self.begin_time) + "\n"

            file_log.add_solution_log(new_solution, message)

        return self.best_solution


    def get_current_best_solution(self):
        current_best = self.best_solution
        
        ages_best = self.local_operators["AGES"].get_current_best_solution()
        if (
            self.solution_is_feasible(ages_best) 
            and self.obj_func.solution_is_better(ages_best, current_best)
        ):
            current_best = ages_best

        lns_best = self.local_operators["LNS"].get_current_best_solution()
        if (
            self.solution_is_feasible(lns_best) 
            and self.obj_func.solution_is_better(lns_best, current_best)
        ):
            current_best = lns_best
        
        sp = self.local_operators["SetPartitionModel"]
        sp_best = sp.get_current_best_solution()
        if (
            self.solution_is_feasible(sp_best) 
            and self.obj_func.solution_is_better(sp_best, current_best)
        ):
            current_best = sp_best

        return current_best




    def print_solution_pos_operator_status(
        self, 
        solution, 
        operator_name, 
        exec_time
    ):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        if (solution_check(solution, self.constraints, self.obj_func)):
            print(
                "SOLUTION IS OK AFTER", 
                operator_name
            )
        else:
            print(
                get_solution_check_complete_data(
                    solution, 
                    self.constraints, 
                    self.obj_func
                )
            )
        print(
            "obj_func, obj_route: ", 
            solution.cost(), 
            ",",
            solution.routes_cost()
        )
        print(
            operator_name,
            "time:", 
            exec_time
        )

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")


    def define_local_searches_operators(self, op_dict):
        return super().define_local_searches_operators(op_dict)


    def stop_criteria_fulfilled(self):
        if (self.stop_criteria == "time"):
            begin_time = self.begin_time
            time_last_it = self.time_last_it
            return self.time_stop_criteria_fulfilled(
                begin_time,
                time_last_it
            )
        elif(self.stop_criteria == "iterations"):
            it = self.iteration
            return self.it_stop_criteria_fulfilled(it)

        raise exceptions.WrongOrUndefinedStopCriteria(self.__name__)


    def time_stop_criteria_fulfilled(self, 
        begin_time,
        time_last_it
    ):
        if (time_last_it - begin_time >= self.max_time):
            return True

        return False


    def it_stop_criteria_fulfilled(self, it):
        if (it >= self.max_it):
            return True

        return False


    def update_route_values(self, route, position, request):
        super().update_route_values(route, position, request)
    

    def get_attr_relation_reader_heuristic(self):
        return {}