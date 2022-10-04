import os
import collections
import json
import multiprocessing
import shutil
import time
import copy
import requests
import math


from .CurrentSolution import CurrentSolution
from .CurrentSolutionUR import CurrentSolutionUR

from src import InstanceData
from src import InstanceDataUR
from src import RequestsStorage
from src import send_request_to_solver
from src.make_requests_dict import make_requests_dicts


semaphore = multiprocessing.BoundedSemaphore(value=1)

base_path = None
shutdown_link = None

def get_log_inputs_path():
    global base_path
    return os.path.join(base_path, "inputs")

def get_log_outputs_path():
    global base_path
    return os.path.join(base_path, "outputs")

def get_log_file_path():
    global base_path
    return os.path.join(base_path, "log.txt")


def create_directory_log_path(log_dir_name, output_path="."):
    global base_path
    if (log_dir_name == None):
        i = 1
        while (os.path.exists(os.path.join(".", "log_" + str(i)))):
            i += 1
        base_path = os.path.join(".", "tests", "log_" + str(i))
    else:
        base_path = os.path.join(output_path, "sr_log", log_dir_name)
    
    inputs_path = get_log_inputs_path()
    outputs_path = get_log_outputs_path()
    log_file = get_log_file_path()

    if (os.path.exists(base_path)):
        for old_run_data in os.listdir(inputs_path):
            file_name = os.path.join(inputs_path, old_run_data)
            os.remove(file_name)
        for old_run_data in os.listdir(outputs_path):
            file_name = os.path.join(outputs_path, old_run_data)
            os.remove(file_name)
    else:
        os.makedirs(base_path)
        os.makedirs(inputs_path)
        os.makedirs(outputs_path)
    with open(log_file, "w"):
        pass
    

def write_on_log(text):
    with open(get_log_file_path(), "a") as log_file:
        break_line = 80 * "-"
        log_file.write(break_line + "\n")
        log_file.write(str(text) + "\n")


def create_time_slices(time_slice_size, horizon):
    number_of_time_slices = int(horizon / time_slice_size)

    time_slices = []
    for i in range(number_of_time_slices):
        time_slice = (i*time_slice_size, (i+1)*time_slice_size)
        time_slices.append(time_slice)

    return time_slices

        

def can_attend_request(request_dict, start_time, horizon):
    request_pair = request_dict["request"]
    pair_service_time = request_dict["services_times"]

    global semaphore
    # semaphore.acquire()
    
    # print("T3 critical")

    depot_to_pick = InstanceData().get_travel_time(
        0, 
        request_pair[0]
    )
    depot_to_pick *= 60
    pick_to_deli = InstanceData().get_travel_time(
        request_pair[0], 
        request_pair[1]
    )
    pick_to_deli *= 60
    
    deli_to_depot = InstanceData().get_travel_time(
        request_pair[1],
        0
    )
    deli_to_depot *= 60
    # print("T3 critical end")

    # semaphore.release()

    travel_time_to_deli = (
        start_time
        + depot_to_pick
        + pair_service_time[0]*60
        + pick_to_deli
    )
        

    minimum_travel_time = (
        travel_time_to_deli
        + pair_service_time[1]*60
        + deli_to_depot
    )

    tw_pick = request_dict["time_windows"][0]
    tw_pick =  (tw_pick[0] * 60, tw_pick[1] * 60)
    tw_deli = request_dict["time_windows"][1]
    tw_deli =  (tw_deli[0] * 60, tw_deli[1] * 60)
    
    # print("hor", horizon)
    # print("start", start_time)
    # print("dep_pic", depot_to_pick)
    # print("to_deli", travel_time_to_deli)
    # print("min_t", minimum_travel_time)
    # print("tws", tw_pick[0], tw_pick[1], tw_deli[0], tw_deli[1])
    
    if (minimum_travel_time > horizon):
        return (False, "INFEASIBLE: TRAVEL TIME > HORIZON")

    if (tw_pick[1] < start_time):
        return (False, "TW FOR PICKUP ALREADY ENDED")
    
    if (tw_pick[1] < start_time + depot_to_pick):
        return (False, "INFEASIBLE TW FOR PICKUP")
    
    if (tw_deli[1] < start_time):
        return (False, "TW FOR DELIVERY ALREADY ENDED")

    if (tw_deli[1] < travel_time_to_deli):
        return (False, "INFEASIBLE TW FOR DELIVERY")
    
    return (True, "OK")


def add_request(request_dict, time_slices, current_time_slice_id):

    ts_size = (time_slices[0][1] - time_slices[0][0])
    horizon = len(time_slices) * ts_size

    # print(request_dict)
    # start_time = 0
    # for i in range(current_time_slice_id):
    #     start_time += ts_size

    # can_attend, message = can_attend_request(
    #     request_dict, 
    #     start_time, 
    #     horizon
    # )

    # if (not can_attend):
    #     return "Request cannot be attended: " + message

    global semaphore
    # semaphore.acquire()
    # print("T2 critical")
    if (request_dict["request"] in RequestsStorage().new_requests):
        write_on_log("IN NEW REQUESTS " + str(request_dict["request"]))
    if (request_dict["request"] in RequestsStorage().all_requests):
        write_on_log("IN ALL REQUESTS " + str(request_dict["request"]))
    
    RequestsStorage().store_new_request(
        tuple(request_dict["request"]), 
        request_dict
    )
    # print("T2 critical end")
    # semaphore.release()

    return "Request Accepted"

def initialize_instance(instance_path, problem):
    if (problem.upper() == "DPDPTWNOC-D"):
        InstanceData(test_instance=instance_path)
        InstanceData().read_data_from_instance()
        CurrentSolution()
    if (problem.upper() == "DPDPTWUR-R"):
        InstanceDataUR(test_instance=instance_path)
        InstanceData().read_data_from_instance()
        CurrentSolutionUR()



def make_copies():
    semaphore.acquire()
    
    all_requests = copy.deepcopy(RequestsStorage().get_all_requests())
    new_requests = copy.deepcopy(RequestsStorage().get_new_requests())

    RequestsStorage().reset_new_requests()


    vehicles_positions = copy.deepcopy(
        CurrentSolution().get_vehicles_positions()
    )

    routes = copy.deepcopy(CurrentSolution().get_routes())

    semaphore.release()


    return (
        all_requests,
        new_requests,
        routes,
        vehicles_positions
    )


def get_non_attended_requests(all_requests, routes, vehicles_position):
    
    parcials = set()
    completed = set()
    for pair in all_requests:
        complete_attended = False
        parcial_attended = False
        for vehicle, route in routes.items():
            vehicle_pos = vehicles_position[vehicle]
            i = 0
            while (i < vehicle_pos and not complete_attended):
                if (route[i] == pair[0]):
                    parcial_attended = True
                elif (route[i] == pair[1]):
                    complete_attended = True
                    parcial_attended = False
                i += 1
            if (parcial_attended or complete_attended):
                break
                    
        if (complete_attended):
            completed.add(pair)
        if (parcial_attended):
            parcials.add(pair)

    # print(parcials, completed)
    non_attended = all_requests - parcials - completed
    return (non_attended, parcials, completed)

def get_non_planned_requests(all_requets, routes):
    non_planned_requests = set()
    for request in all_requets:
        found = False
        for vehicle, route in routes.items():
            for i in route:
                if (i in request):
                    found = True
        if (not found):
            non_planned_requests.add(request)

    return non_planned_requests


def make_mapping_dicts(all_requests_ids):
    orig_to_mapped = {}
    mapped_to_orig = {}

    for i, request in enumerate(all_requests_ids):
        pickup = i + 1
        delivery = pickup + len(all_requests_ids)

        mapped_request = (pickup, delivery)

        orig_to_mapped[request] = mapped_request
        mapped_to_orig[mapped_request] = request

    # print({k: v for k, v in sorted(
    #     mapped_to_orig.items(), 
    #     key=lambda item: item[1]
    # )})

    return (orig_to_mapped, mapped_to_orig)


def make_requests_data_dict(all_requests, orig_to_mapped, non_attended_ids):

    requests_data_dict = InstanceData().make_requests_data_dict(
        all_requests, 
        orig_to_mapped, 
        non_attended_ids
    )

    return requests_data_dict


def make_matrices_data_dict(all_requests, mapped_to_orig):
    n_points = len(all_requests) * 2 + 1
    distance_matrix = {}
    time_matrix = {}

    mapping_picks, mapping_delis = divide_pds_mapped_ids(mapped_to_orig)
    vertices_mapping = {**mapping_picks, **mapping_delis}

    for i in range(n_points):
        distance_matrix[i] = {}
    for i in range(1, n_points):
        for j in range(1, n_points):
            # semaphore.acquire()

            distance_matrix[0][i] = InstanceData().get_travel_cost(
                0, 
                vertices_mapping[i]
            )
            distance_matrix[i][0] = InstanceData().get_travel_cost(
                vertices_mapping[i], 
                0
            )

            distance_matrix[0][j] = InstanceData().get_travel_cost(
                0, 
                vertices_mapping[j]
            )
            distance_matrix[j][0] = InstanceData().get_travel_cost(
                vertices_mapping[j], 
                0
            )

            distance_matrix[i][j] = InstanceData().get_travel_cost(
                vertices_mapping[i], 
                vertices_mapping[j]
            )
            distance_matrix[j][i] = InstanceData().get_travel_cost(
                vertices_mapping[j], 
                vertices_mapping[i]
            )
            
            # semaphore.release()
    distance_matrix[0][0] = 0
    
    for i in range(n_points):
        time_matrix[i] = {}
    for i in range(1, n_points):
        for j in range(1, n_points):
            # semaphore.acquire()

            time_matrix[0][i] = InstanceData().get_travel_time(
                0, 
                vertices_mapping[i]
            )
            time_matrix[i][0] = InstanceData().get_travel_time(
                vertices_mapping[i], 
                0
            )

            time_matrix[0][j] = InstanceData().get_travel_time(
                0, 
                vertices_mapping[j]
            )
            time_matrix[j][0] = InstanceData().get_travel_time(
                vertices_mapping[j], 
                0
            )

            time_matrix[i][j] = InstanceData().get_travel_time(
                vertices_mapping[i], 
                vertices_mapping[j]
            )
            time_matrix[j][i] = InstanceData().get_travel_time(
                vertices_mapping[j], 
                vertices_mapping[i]
            )

            # semaphore.release()

    time_matrix[0][0] = 0
    
    matrices_dict = {}
    matrices_dict["distance_matrix"] = distance_matrix
    matrices_dict["time_matrix"] = time_matrix

    return matrices_dict

def make_instance_data_dict():
    # semaphore.acquire()

    instance_data = InstanceData().make_instance_data_dict()

    # capacity = InstanceData().capacity
    # depot = InstanceData().depot
    # planning_horizon = InstanceData().horizon
    # time_windows_size = InstanceData().tw_size
    # fleet_size = InstanceData().fleet_size
    
    # semaphore.release()

    # instance_data = {}

    # instance_data["capacity"] = capacity
    # instance_data["depot"] = depot
    # instance_data["planning_horizon"] = planning_horizon
    # instance_data["time_windows_size"] = time_windows_size
    # instance_data["fleet_size"] = fleet_size

    return instance_data

def make_current_routes_data(
    routes, 
    predicted_positions, 
    orig_to_mapped_pick, 
    orig_to_mapped_deli
):
    data = CurrentSolution().make_current_routes_data(
        routes, 
        predicted_positions, 
        orig_to_mapped_pick, 
        orig_to_mapped_deli
    )

    return data


def divide_pds_mapped_ids(mapping):
    pickups_mapping = {}
    deliveries_mapping = {}
    
    for unmapped, mapped in mapping.items():
        pickups_mapping[unmapped[0]] = mapped[0]
        deliveries_mapping[unmapped[1]] = mapped[1]    

    return (pickups_mapping, deliveries_mapping)


def make_input_dict(
    all_requests, 
    routes, 
    non_attended_ids, 
    predicted_positions
):
    all_requests_ids = set(all_requests.keys())
    orig_to_mapped, mapped_to_orig = make_mapping_dicts(all_requests_ids)
    
    orig_to_mapped_pickups, orig_to_mapped_deliveries = divide_pds_mapped_ids(
        orig_to_mapped
    )
    mapped_to_orig_pickups, mapped_to_orig_deliveries = divide_pds_mapped_ids(
        mapped_to_orig
    )
    
    # orig_to_mapped_pickups = {}
    # orig_to_mapped_deliveries = {}
    # for orig, mapped in orig_to_mapped.items():
    #     orig_to_mapped_pickups[orig[0]] = mapped[0]
    #     orig_to_mapped_deliveries[orig[1]] = mapped[1]
    
    # mapped_to_orig_pickups = {}
    # mapped_to_orig_deliveries = {}
    # for mapped, orig in mapped_to_orig.items():
    #     mapped_to_orig_pickups[mapped[0]] = orig[0]
    #     mapped_to_orig_deliveries[mapped[1]] = orig[1]


    instance_data = make_instance_data_dict()
    requests_data = make_requests_data_dict(
        all_requests, 
        orig_to_mapped, 
        non_attended_ids
    )
    
    for key, value in requests_data.items():
        instance_data[key] = value

    matrices_data = make_matrices_data_dict(all_requests, mapped_to_orig)
    for key, value in matrices_data.items():
        instance_data[key] = value

    current_routes_data = make_current_routes_data(
        routes, 
        predicted_positions,
        orig_to_mapped_pickups,
        orig_to_mapped_deliveries
    )
    for key, value in current_routes_data.items():
        instance_data[key] = value

    # print(orig_to_mapped)
    # print(mapped_to_orig)
    return (orig_to_mapped, mapped_to_orig, instance_data)


def write_input_dict(instance_data, current_slice_id):
    input_dir_path = get_log_inputs_path()

    global base_path
    instance_dir = os.path.basename(base_path)

    file_name = str(instance_dir) + "_slice_" + str(current_slice_id) + ".json"
    file_path = os.path.join(input_dir_path, file_name)
    
    with open(file_path, "w") as slice_instance_file:
        slice_instance_file.write(json.dumps(instance_data))

    return file_path


def send_request(input_file_path, time_limit, output_path, problem):
    global shutdown_link

    if (problem.upper() == "DPDPTWUR-R"):
        problem = "dpdptwhf-r"
    if (problem.upper() == "DPDPTWNOC-D"):
        problem = "dpdptwlf-d"
    write_on_log("AAAAAAAAAAAAAAAAAAAAAAAA")
    result = send_request_to_solver.send_request(
        problem, 
        input_file_path, 
        time_limit,
        shutdown_link,
        output_path
    )
    write_on_log(result)
    if (type(result) != dict):
        raise(Exception("NoSolutionFound"))
    write_on_log("AAAAAAAAAAAAAAAAAAAAAAAA")

    return result


def store_new_solution(new_solution, mapping):
    routes = {}
    costs = {}
    
    mapping_picks, mapping_delis = divide_pds_mapped_ids(mapping)

    vertices_mapping = {**mapping_picks, **mapping_delis}
    for route_id, route in new_solution["routes"].items():
        routes[int(route_id)] = [
            vertices_mapping[vertex]
            for vertex in route
        ]
        costs[int(route_id)] = new_solution["costs"][route_id]

    # semaphore.acquire()
    CurrentSolution().reset_routes(routes, costs, new_solution)
    # semaphore.release()



def solve_time_slice(
    ts_size, 
    time_limit, 
    current_ts_id, 
    data,
    output_path,
    problem
):
    
    all_requests = data[0]
    new_requests = data[1]
    routes = data[2]
    vehicles_positions = data[3]

    if (len(all_requests) < 1):
        # print("No new requests to attend")
        return

    all_requests_ids = set(all_requests.keys())
    # new_requests_ids = set(new_requests.keys())
    
    # semaphore.acquire()
    CurrentSolution().calculate_end_exec_predicted_positions(
        routes,
        ts_size,
        current_ts_id    
    )
    # semaphore.release()

    predicted_positions = CurrentSolution().get_predicted_positions()

    # non_attended_ids, parcials_ids, completed_ids = get_non_attended_requests(
    #     all_requests_ids, 
    #     routes,
    #     predicted_positions
    # )

    non_attended_ids = get_non_planned_requests(
        all_requests_ids, 
        routes
    )

    orig_to_mapped, mapped_to_orig, input_dict = make_input_dict(
        all_requests, 
        routes, 
        non_attended_ids, 
        predicted_positions
    )

    input_file_path = write_input_dict(input_dict, current_ts_id)
    
    new_solution = send_request(
        input_file_path, 
        time_limit, 
        output_path, 
        problem
    )
    # print(new_solution)
    
    store_new_solution(new_solution, mapped_to_orig)

    # semaphore.acquire()

    CurrentSolution().write_solution(get_log_outputs_path(), current_ts_id)
    write_on_log(
        "SOLUTION FOR SLICE " 
        + str(current_ts_id) 
        + " WRITTEN ON DIRECTORY " 
        + get_log_outputs_path()
    )

    # semaphore.release()



def solve_time_slices_problems(
    time_slices, 
    current_time_slice_id, 
    time_limit,
    problem,
    log_dir_name=None,
    shtdn_link=None,
    output_path=None
):
    global shutdown_link
    shutdown_link = shtdn_link
    time_slices_size = time_slices[0][1] - time_slices[0][0]
    
    # time_slices_size = 5
    # time_limit = 2
    time_slices = time_slices[:3]

    # print(len(time_slices))
    
    while (current_time_slice_id < len(time_slices)):
        print("TIME SLICE " + str(current_time_slice_id))
        time.sleep(time_slices_size-time_limit)
        
        global semaphore
        
        # semaphore.acquire()

        data = make_copies()
        
        # semaphore.release()
        
        solve_time_slice(
            time_slices_size, 
            time_limit, 
            current_time_slice_id, 
            data,
            output_path,
            problem
        )
        
        current_time_slice_id += 1


    if (shutdown_link is not None):
        requests.get(shutdown_link)
    
    
def solve_from_instance(
    time_slices, 
    time_limit, 
    problem,
    log_dir_name, 
    output_path
):
    start_time = time.time()
    
    time_slice_size = time_slices[0][1] - time_slices[0][0]

    requests_dicts = make_requests_dicts(InstanceData().test_instance, problem)
    current_requets_dicts = requests_dicts
    next_requets_dicts = []

    time_limit_in_minutes = math.ceil(time_limit/60)

    time_sorted_requests = [
        k for k in 
        sorted(
            requests_dicts, 
            key=lambda item: item["time_in"]
        )
    ]

    position_in_sorted = 0

    solution_not_found = False

    for i in range(len(time_slices)):
        if (solution_not_found):
            continue
        current_time_slice = i+1
        write_on_log(
            "TIME SLICE " 
            + str(current_time_slice) 
            + "(time: " 
            + str(time.time() - start_time)
            + ")"
        )


        last_ts_end = time_slice_size * (current_time_slice-1)
        current_ts_end = time_slice_size * (current_time_slice)
        starting_solver_time = current_ts_end - time_limit_in_minutes
        # starting_solver_time = current_ts_end
        last_ts_solver_start = last_ts_end - time_limit_in_minutes
        # last_ts__solver_start = last_ts_end

        added_requests = []

        if (position_in_sorted < len(time_sorted_requests)):
            request = time_sorted_requests[position_in_sorted]
            while (
                request["time_in"] <= starting_solver_time
                and position_in_sorted < len(time_sorted_requests)
            ):
                added_requests.append(request["request"])
                add_request(request, time_slices, current_time_slice)
                position_in_sorted += 1
                if (position_in_sorted < len(time_sorted_requests)):
                    request = time_sorted_requests[position_in_sorted]

        write_on_log("REQUESTS ADDED: " + str(added_requests))

        # for request in current_requets_dicts:
        #     if (
        #         request["time_in"] <= last_ts_solver_start 
        #         and current_time_slice > 1
        #     ):
        #         continue
        #     if (
        #         request["time_in"] 
        #         > starting_solver_time
        #     ):
        #         next_requets_dicts.append(request)
        #         continue
        #     add_request(request, time_slices, current_time_slice)
        
        current_requets_dicts = [
            item["request"] 
            for item in time_sorted_requests[:position_in_sorted]
        ]
        
        write_on_log(
            "NUMBER OF REQUESTS ON TIME SLICE " 
            + str(i) 
            + ": "
            + str(len(current_requets_dicts))
            + "\n"
            + "REQUESTS FOR TIME SLICE\n\n" 
            + str(current_requets_dicts)
        )
        

        data = make_copies()
        
        write_on_log("COPIES: " + str(data))
        
        write_on_log(
            "CALLING SOLVER "
            + "(time: " 
            + str(time.time() - start_time)
            + ")"
        )

        try:
            solve_time_slice(
                time_slice_size, 
                time_limit, 
                current_time_slice, 
                data,
                output_path, 
                problem
            )
        except Exception as ex:
            if (str(ex) != "NoSolutionFound"):
                raise ex

            solution_not_found = True   


        write_on_log(
            "FINISHED SLICE "
            + str(current_time_slice)
            + " "
            + "(time: " 
            + str(time.time() - start_time)
            + ")"
        )

        current_requets_dicts
        # print(current_requets_dicts)
