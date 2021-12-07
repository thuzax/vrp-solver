import hyperopt


constructive_params = {}


def get_params_dict():
    global constructive_params
    return constructive_params


def constructive_options():
    choice = hyperopt.hp.choice(
        "constructive_opt",
        ["BasicGreedy", "WBasicGreedy"]
    )
    
    global constructive_params
    constructive_params["constructive_opt"] = choice

    return choice



def basic_greedy():
    data = {
        "obj_func_name" : "ObjVehicles",
        "constraints_names" : [
            "AttendAllRequests",
            "PickupDeliveryConstraint",
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    return data
    
def w_basic_greedy():
    data =  {
        "obj_func_name" : "ObjVehicles",
        "constraints_names" : [
            "AttendAllRequests",
            "PickupDeliveryConstraint",
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    return data