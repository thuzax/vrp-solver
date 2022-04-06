import collections
import json
import multiprocessing
import time
import copy

from .CurrentSolution import CurrentSolution

from src import InstanceData
from src import RequestsStorage


semaphore = multiprocessing.BoundedSemaphore(value=1)

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
    semaphore.acquire()
    
    print("T3 critical")

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
    print("T3 critical end")

    semaphore.release()

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

    start_time = 0
    for i in range(current_time_slice_id):
        start_time += ts_size

    can_attend, message = can_attend_request(
        request_dict, 
        start_time, 
        horizon
    )

    if (not can_attend):
        return "Request cannot be attended: " + message

    global semaphore
    semaphore.acquire()
    print("T2 critical")
    RequestsStorage().store_new_request(
        tuple(request_dict["request"]), 
        request_dict
    )
    print("T2 critical end")
    semaphore.release()
    time.sleep(1)

    return "Request Accepted"

def initialize_instance(instance_path):
    InstanceData(test_instance=instance_path)
    InstanceData().read_data_from_instance()



def make_copies():
    all_requests = copy.deepcopy(RequestsStorage().get_all_requests())
    new_requests = copy.deepcopy(RequestsStorage().get_new_requests())

    RequestsStorage().reset_new_requests()


    vehicles_positions = copy.deepcopy(
        CurrentSolution().get_vehicles_positions()
    )

    routes = copy.deepcopy(CurrentSolution().get_routes())

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

    print(parcials, completed)
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

    return (orig_to_mapped, mapped_to_orig)


def make_requests_data_dict(all_requests, orig_to_mapped, non_attended_ids):
    points = {}
    
    semaphore.acquire()
    points[0] = InstanceData().get_depot_point()
    semaphore.release()
    
    demands = {}
    services_times = {}
    time_windows_pd = {}
    pickups_and_deliveries = []

    for orig, mapped in orig_to_mapped.items():
        request = all_requests[orig]
        
        points[mapped[0]] = request["points"][0]
        points[mapped[1]] = request["points"][1]

        
        if (orig in non_attended_ids):
            pickups_and_deliveries.append(mapped)
        
        demands[mapped[0]] = request["demands"][0]
        demands[mapped[1]] = request["demands"][1]

        services_times[mapped[0]] = request["services_times"][0]
        services_times[mapped[1]] = request["services_times"][1]

        time_windows_pd[mapped[0]] = request["time_windows"][0]
        time_windows_pd[mapped[1]] = request["time_windows"][1]

    requests_data_dict = {}
    
    requests_data_dict["number_of_points"] = len(points)

    points = dict(collections.OrderedDict(sorted(points.items())))
    requests_data_dict["points"] = points

    demands = dict(collections.OrderedDict(sorted(demands.items())))
    requests_data_dict["demands"] = demands

    services_times = dict(
        collections.OrderedDict(sorted(services_times.items()))
    )
    requests_data_dict["services_times"] = services_times
    
    time_windows_pd = dict(
        collections.OrderedDict(sorted(time_windows_pd.items()))
    )
    requests_data_dict["time_windows_pd"] = time_windows_pd
    
    requests_data_dict["pickups_and_deliveries"] = pickups_and_deliveries


    return requests_data_dict


def make_matrices_data_dict(all_requests):
    n_points = len(all_requests) * 2 + 1
    distance_matrix = {}
    time_matrix = {}

    for i in range(n_points):
        distance_matrix[i] = {}
    for i in range(n_points):
        for j in range(n_points):
            semaphore.acquire()

            distance_matrix[0][i] = InstanceData().get_travel_cost(0, i)
            distance_matrix[i][0] = InstanceData().get_travel_cost(i, 0)

            distance_matrix[0][j] = InstanceData().get_travel_cost(0, j)
            distance_matrix[j][0] = InstanceData().get_travel_cost(j, 0)

            distance_matrix[i][j] = InstanceData().get_travel_cost(i, j)
            distance_matrix[j][i] = InstanceData().get_travel_cost(j, i)
            
            semaphore.release()
    
    for i in range(n_points):
        time_matrix[i] = {}
    for i in range(n_points):
        for j in range(n_points):
            semaphore.acquire()

            time_matrix[0][i] = InstanceData().get_travel_time(0, i)
            time_matrix[i][0] = InstanceData().get_travel_time(i, 0)

            time_matrix[0][j] = InstanceData().get_travel_time(0, j)
            time_matrix[j][0] = InstanceData().get_travel_time(j, 0)

            time_matrix[i][j] = InstanceData().get_travel_time(i, j)
            time_matrix[j][i] = InstanceData().get_travel_time(j, i)

            semaphore.release()

    matrices_dict = {}
    matrices_dict["distance_matrix"] = distance_matrix
    matrices_dict["time_matrix"] = time_matrix

    return matrices_dict

def make_instance_data_dict():
    semaphore.acquire()

    capacity = InstanceData().capacity
    depot = InstanceData().depot
    planning_horizon = InstanceData().horizon
    time_windows_size = InstanceData().tw_size
    
    semaphore.release()

    instance_data = {}

    instance_data["capacity"] = capacity
    instance_data["depot"] = depot
    instance_data["planning_horizon"] = planning_horizon
    instance_data["time_windows_size"] = time_windows_size

    return instance_data

def make_current_routes_data(
    routes, 
    predicted_positions, 
    orig_to_mapped_pick, 
    orig_to_mapped_deli
):
    fixed = []
    for vehicle, route in routes.items():
        predicted_position = predicted_positions[vehicle]
        route_mapped = []
        for vertex_id in route:
            if (vertex_id in orig_to_mapped_pick):
                route_mapped.append(orig_to_mapped_pick[vertex_id])
            elif (vertex_id in orig_to_mapped_deli):
                route_mapped.append(orig_to_mapped_deli[vertex_id])
        
        fixed.append({
            "route" : route_mapped,
            "start" : predicted_position
        })

    current_routes_data = {}
    current_routes_data["fixed"] = fixed
    
    return current_routes_data


def make_input_json(
    all_requests, 
    routes, 
    non_attended_ids, 
    predicted_positions
):
    all_requests_ids = set(all_requests.keys())
    orig_to_mapped, mapped_to_orig = make_mapping_dicts(all_requests_ids)
    orig_to_mapped_pickups = {}
    orig_to_mapped_deliveries = {}
    for orig, mapped in orig_to_mapped.items():
        orig_to_mapped_pickups[orig[0]] = mapped[0]
        orig_to_mapped_deliveries[orig[1]] = mapped[1]
    
    mapped_to_orig_pickups = {}
    mapped_to_orig_deliveries = {}
    for mapped, orig in mapped_to_orig.items():
        mapped_to_orig_pickups[mapped[0]] = orig[0]
        mapped_to_orig_deliveries[mapped[1]] = orig[1]


    instance_data = make_instance_data_dict()
    requests_data = make_requests_data_dict(
        all_requests, 
        orig_to_mapped, 
        non_attended_ids
    )
    for key, value in requests_data.items():
        instance_data[key] = value

    matrices_data = make_matrices_data_dict(all_requests)
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
    try:
        open("../test.json", "r")
    except:
        with open("../test.json", "w") as slice_instance_file:
            slice_instance_file.write(json.dumps(instance_data, indent=2))



def solve_time_slice(ts_size, current_ts_id, data):
    
    all_requests = data[0]
    new_requests = data[1]
    routes = data[2]
    vehicles_positions = data[3]

    if (len(all_requests) < 1):
        time.sleep(ts_size)
        print("No requests to attend")
        return

    all_requests_ids = set(all_requests.keys())
    new_requests_ids = set(new_requests.keys())
    
    semaphore.acquire()
    CurrentSolution().calculate_end_exec_predicted_positions(
        routes,
        ts_size,
        current_ts_id    
    )
    semaphore.release()

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

    make_input_json(
        all_requests, 
        routes, 
        non_attended_ids, 
        predicted_positions
    )



def solve_time_slices_problems(time_slices, current_time_slice_id):
    time_slices_size = time_slices[0][1] - time_slices[0][0]
    
    time_slices_size = 5
    time_slices = time_slices[:3]
    
    # time.sleep(time_slices_size)
    time.sleep(30)
    

    while (current_time_slice_id < len(time_slices)):
        global semaphore
        semaphore.acquire()
        print("T1 crictical")
        data = make_copies()
        print("T1 critical end")
        semaphore.release()

        solve_time_slice(time_slices_size, current_time_slice_id, data)
        time.sleep(5)
        current_time_slice_id += 1

    