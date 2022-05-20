def reinsertion_options(params):
    opts = ["KRegret", "WKRegret"]
    choice = opts[params["reinsertion_opt"]]
    return choice

def k_regret(params):
    data = {
        "non_insertion_cost" : 9999999999999,
        "use_modification" : False,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    return data

def k_regret_dynamic(params):
    data = {
        "non_insertion_cost" : 9999999999999,
        "use_modification" : False,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    return data

def k_regret_dlf(params):
    data = {
        "non_insertion_cost" : 9999999999999,
        "use_modification" : False,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    return data

def k_regret_dlhf(params):
    data = {
        "non_insertion_cost" : 9999999999999,
        "use_modification" : False,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests",
            "HeterogeneousFleet"
        ]
    }
    return data


def w_k_regret(params):
    data = {
        "non_insertion_cost" : 9999999999999,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    return data

def w_k_regret_dynamic(params):
    data = {
        "non_insertion_cost" : 9999999999999,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    return data

def w_k_regret_dlf(params):
    data = {
        "non_insertion_cost" : 9999999999999,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    return data


def w_k_regret_dlhf(params):
    data = {
        "non_insertion_cost" : 9999999999999,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests",
            "HeterogeneousFleet"
        ]
    }
    return data




def random_insertion(params):
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    return data
    
def random_insertion_dynamic(params):
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    return data

def random_insertion_dlf(params):
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    return data
    

def random_insertion_dlhf(params):
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests",
            "HeterogeneousFleet"
        ]
    }
    return data


def reinsertion_data(params, problem):
    k_regret_name = "KRegret"
    k_regret = None
    wk_regret_name = "WKRegret"
    wk_regret = None
    random_insertion_name = "RandomInsertion"
    random_insertion = None

    if (problem == "PDPTW"):
        k_regret = k_regret(params)
        wk_regret = w_k_regret(params)
        random_insertion = random_insertion(params)
    if (problem == "DPDPTW"):
        k_regret = k_regret_dynamic(params)
        wk_regret = w_k_regret_dynamic(params)
        random_insertion = random_insertion_dynamic(params)
    if (problem == "DPDPTWLF-R"):
        k_regret = k_regret_dlf(params)
        wk_regret = w_k_regret_dlf(params)
        random_insertion = random_insertion_dlf(params)
    if (problem == "DPDPTWLHF-R"):
        k_regret = k_regret_dlhf(params)
        wk_regret = w_k_regret_dlhf(params)
        random_insertion = random_insertion_dlhf(params)

    algs_data = {
        k_regret_name : k_regret,
        wk_regret_name : wk_regret,
        random_insertion_name : random_insertion
    }
    return algs_data
