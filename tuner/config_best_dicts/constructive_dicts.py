def basic_greedy(params):
    ins_opt = ["fi", "kr", "wkr"]
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "AttendAllRequests",
            "PickupDeliveryConstraint",
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ],
        "insertion_heuristic_code" : (
            ins_opt[params["insertion_heuristic_greedy_heuristic"]]
        )
    }
    return data

def basic_greedy_dynamic(params):
    data = basic_greedy(params)
    data["constraints_names"] =  [
        "PickupDeliveryConstraint",
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]
    

    return data

def basic_greedy_limited_fleet(params):
    data = basic_greedy(params)
    data["constraints_names"] = [
        "PickupDeliveryConstraint",
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]

    data["obj_func_name"] = "ObjRequestsPDPTW"

    return data

def basic_greedy_limited_heterogeneous_fleet(params):
    data = basic_greedy(params)
    data["constraints_names"] = [
        "PickupDeliveryConstraint",
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]
    return data

def constructive_data(params, problem):
    if (problem == "PDPTW"):
        algs_data = {
            "BasicGreedy" : basic_greedy(params)
        }
    if (problem == "DPDPTW"):
        algs_data = {
            "BasicGreedy" : basic_greedy_dynamic(params)
        }
    if (problem == "DPDPTWLF-R"):
        algs_data = {
            "BasicGreedyLimitedFleet" : (
                basic_greedy_limited_fleet(params)
            )
        }
    if (problem == "DPDPTWLHF-R"):
        algs_data = {
            "BasicGreedyLimitedHeterogeneousFleet" : (
                basic_greedy_limited_heterogeneous_fleet(params)
            )
        }

    return algs_data