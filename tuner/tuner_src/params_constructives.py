import hyperopt


constructive_params = {}


def get_params_dict():
    global constructive_params
    return constructive_params




def basic_greedy():
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "AttendAllRequests",
            "PickupDeliveryConstraint",
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ],
        "insertion_heuristic_code" : (
            hyperopt.hp.choice(
                "insertion_heuristic_greedy_heuristic",
                ["kr", "wkr"]
            )
        )
    }
    return data

def basic_greedy_dynamic():
    data = basic_greedy()
    data["constraints_names"] =  [
        "PickupDeliveryConstraint",
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]
    

    return data

def basic_greedy_limited_fleet():
    data = basic_greedy()
    data["constraints_names"] = [
        "PickupDeliveryConstraint",
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]

    data["obj_func_name"] = "ObjRequestsPDPTW"

    return data

def basic_greedy_limited_heterogeneous_fleet():
    data = basic_greedy()
    data["constraints_names"] = [
        "PickupDeliveryConstraint",
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]
    return data