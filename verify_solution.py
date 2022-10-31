import copy
import sys
import json

from scipy.sparse.csgraph import maximum_bipartite_matching
from scipy.sparse import csr_matrix

import numpy
import collections

text = ""

def read_solution(solution_file_name, all_sol):
        with open(solution_file_name, "r") as sol_file:
            data = json.loads(sol_file.read())
        
        if (not all_sol):
            solution = [data["solution"]]
            return solution
        
        return data
    
    
    

def read_input(input_file_name):
    with open(input_file_name, "r") as input_file:
        data = json.loads(input_file.read())

    return data


def problem_has_capacity_constraint(problem):
    if (problem == "DPDPTWNoC-D"):
        return False
    return True


def problem_needs_to_attend_all_requests(problem):
    if (
        problem == "PDPTW" 
        or problem == "DPDPTW"
        or problem == "DPDPTWNoC-D"
    ):
        return True
    return False

def problem_has_limited_fleet(problem):
    if (
        problem == "DPDPTW-R" 
        or problem == "DPDPTWNoC-D" 
        or problem == "DPDPTWUR-R"
    ):
        return True
    return False

def problem_is_dynamic(problem):
    if (
        problem == "DPDPTW-R" 
        or problem == "DPDPTWNoC-D" 
        or problem == "DPDPTWUR-R" 
        or problem == "DPDPTW"
    ):
        return True
    return False


def pick_and_deli_feasible(solution, n_requests):
    global text
    found_pickup = [False for i in range(n_requests)]
    pickup_route = [-1 for i in range(n_requests)]
    for route_id, route in solution["routes"].items():
        for point_id in route:
            point_id = int(point_id)
            if (point_id <= n_requests):
                found_pickup[point_id-1] = True
                pickup_route[point_id-1] = route_id
            
            elif (not found_pickup[point_id-n_requests-1]):
                text += str(point_id)
                return False
            
            elif (pickup_route[point_id-n_requests-1] != route_id):
                return False

    return True


def attend_all_requests_once(solution, n_requets):
    global text
    found_point = [False for i in range(n_requets*2)]
    total = 0
    for route in solution["routes"].values():
        total += len(route)
        for point_id in route:
            point_id = int(point_id)
            if (found_point[point_id-1]):
                return False
            found_point[point_id-1] = True
    
    return all(found_point)


def capacity_and_demands_respected(solution, max_capacity, demands):
    global text
    for route in solution["routes"].values():
        sum_capacity = 0
        for point_id in route:
            sum_capacity += demands[str(point_id)]
            if (sum_capacity > max_capacity):
                return False
        if (sum_capacity != 0):
            return False
    return True


def time_is_respected(solution, tws, services, horizon, time_matrix, depot):
    global text
    for route in solution["routes"].values():
        arrival = 0
        before = depot
    
        for point_id in route:
            arrival += time_matrix[str(before)][str(point_id)]
            if (arrival < tws[str(point_id)][0]):
                arrival = tws[str(point_id)][0]
            if (arrival > tws[str(point_id)][1]):
                text += "TW" + "\n"
                return False
            before = point_id
            arrival += services[str(before)]
    
        arrival += time_matrix[str(before)][str(depot)]
        if (arrival > horizon):
            text += "HORIZON" + "\n"
            return False
    
    return True


def fleet_size_respected(solution, input_data, problem):
    global text
    if (problem == "DPDPTWUR-R"):
        fleets = input_data["fleet"]
        total_fleet = 0
        for fleet in fleets:
            total_fleet += fleet[0]
        
        n_routes = len(solution["routes"])

        if (total_fleet < n_routes):
            text += "FLEET SIZE TOO SMALL" + "\n"
            return False


        points_type = input_data["attendance_type"]
        routes_with_type = {}
        fleet_cannot_attend = {}
        fleet_can_attend = {}

        for fleet in fleets:

            fleet_type = fleet[1]
            type_key = tuple(fleet_type)
            routes_with_type[type_key] = 0
            fleet_cannot_attend[type_key] = set()
            fleet_can_attend[type_key] = set()
            fleet_type = set(fleet_type)

            for i, route in solution["routes"].items():
                for point_id in route:
                    point_type = points_type[str(point_id)]
                    
                    if (point_type not in fleet_type):
                        fleet_cannot_attend[type_key].add(i)
                        break
                
                if (i not in fleet_cannot_attend[type_key]):
                    fleet_can_attend[type_key].add(i)

        bpmatrix = [
            [0 for i in range(len(solution["routes"]))]
            for j in range(total_fleet)
        ]
        start_line = 0
        last_fleet_line = 0
        for fleet in fleets:
            type_key = tuple(fleet[1])
            
            start_line = last_fleet_line
            last_fleet_line += fleet[0]
            
            for i in range(start_line, last_fleet_line):
                for j in fleet_can_attend[type_key]:
                    j = int(j)
                    bpmatrix[i][j] = 1
        
        matching = maximum_bipartite_matching(
            csr_matrix(bpmatrix), 
            perm_type="column"
        )

        counted_dict = dict(collections.Counter(list(matching)))
        no_matched = 0
        if (-1 in counted_dict):
            no_matched = counted_dict[-1]
        
        if (total_fleet - n_routes < no_matched):
            text += "FLEET CAN'T ATTEND ALL ROUTES" + "\n"
            return False

    if (problem == "DPDPTW-R" or problem == "DPDPTWNoC-D"):
        fleet_size = input_data["fleet_size"]
        n_routes = len(solution["routes"])
        if (fleet_size < n_routes):
            text += "FLEET SIZE TOO SMALL" + "\n"
            return False
    return True


def fixed_requests_are_respected(solution, fixed_requests, n_requests):
    global text
    found_fixed = set()
    
    for fixed_request in fixed_requests:
        fixed_route = fixed_request["route"]
        start = fixed_request["start"]

        fixed_route_set = set(copy.deepcopy(fixed_route))

        for route in solution["routes"].values():
            found_fixed_in_route = False
            for i in range(start+1):
                if (i >= len(route)):
                    if (found_fixed_in_route):
                        return False
                    continue
                point_id = route[i]
                is_pickup = (point_id <= n_requests)
                if (is_pickup and (point_id in fixed_route_set)):
                    if ((point_id + n_requests) not in fixed_route_set):
                        text += "FIXED REQUESTS" + "\n"
                        return False
                    found_fixed.add(point_id)
                    found_fixed.add(point_id + n_requests)
                    found_fixed_in_route = True
            
    all_fixed = set().union(*[
        frozenset(fixed_request["route"][:fixed_request["start"]+1])
        for fixed_request in fixed_requests
    ])

    for point in all_fixed:
        if (point not in found_fixed):
            text += "FIXED REQUESTS" + "\n"
            return False

    return True


def solution_is_feasible(solution, input_data, problem):
    global text
    n_requests = int(input_data["number_of_points"]/2)
    if (not pick_and_deli_feasible(solution, n_requests)):
        text += "PICK -> DELI" + "\n"
        return False
    
    if (problem_has_capacity_constraint(problem)):
        demands = input_data["demands"]
        capacity = input_data["capacity"]
        if (not capacity_and_demands_respected(solution, capacity, demands)):
            text += "CAPACITY OR DEMANDS" + "\n"
            return False

    time_windows = input_data["time_windows_pd"]
    services = input_data["services_times"]
    horizon = input_data["planning_horizon"]
    time_matrix = input_data["time_matrix"]
    depot = input_data["depot"]
    if (
        not time_is_respected(
            solution, 
            time_windows, 
            services, 
            horizon, 
            time_matrix,
            depot
        )
    ):
        text += "TIME" + "\n"
        return False


    if (problem_needs_to_attend_all_requests(problem)):
        if (not attend_all_requests_once(solution, n_requests)):
            text += "ALL REQUESTS" + "\n"
            return False

    if (problem_has_limited_fleet(problem)):
        if (not fleet_size_respected(solution, input_data, problem)):
            text += "FLEET SIZE" + "\n"
            return False

    if (problem_is_dynamic(problem)):
        if (
            not fixed_requests_are_respected(
                solution, 
                input_data["fixed"],
                n_requests
            )
        ):
            text += "DYNAMIC" + "\n"
            return False
        

    return True

def verify(args):
    global text
    text = ""
    all_sol = False
    # print(args)
    if (len(args) > 3):
        all_sol = True if args[3] == "-a" else False

    input_file_name = args[0]
    solution_file_name = args[1]
    problem = args[2]

    solutions = read_solution(solution_file_name, all_sol)
    if (solutions == None or len(solutions) == 0):
        text += "NO SOLUTION FOUND" + "\n"

    input_data = read_input(input_file_name)

    for i, solution in enumerate(solutions):
        if (not solution_is_feasible(solution, input_data, problem)):
            if (all_sol):
                text += "solution " + str(i) + " not feasible" + "\n"
            else:
                text += "solution not feasible" + "\n"
            continue
        
        if (all_sol):
            text += ("solution " + str(i) + " feasible") + "\n"
        else:
            text += "solution feasible" + "\n"
        

    return text

if __name__=="__main__":
    if (len(sys.argv) < 4):
        print("Needs json input file, json solution file and problem")
        print("Problems: PDPTW ; DPDPTW ; DPDPTWNoC-D ;  DPDTW-R ; DPDPTWUR-R")
        exit(0)
    print(verify(sys.argv[1:]))
    