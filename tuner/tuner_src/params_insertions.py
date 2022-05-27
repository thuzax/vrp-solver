import hyperopt

insertion_params = {}



def get_params_dict():
    global insertion_params
    return insertion_params

def reinsertion_options():
    choice = hyperopt.hp.choice(
        "reinsertion_opt",
        ["KRegret", "WKRegret"]
    )
    
    global insertion_params
    insertion_params["reinsertion_opt"] = choice
    
    return choice

def k_regret():
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

def k_regret_dynamic():
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

def k_regret_dlf():
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

def k_regret_dlhf():
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


def w_k_regret():
    constraints_list = [

    ]
    data = {
        "non_insertion_cost" : 9999999999999,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    return data

def w_k_regret_dynamic():
    constraints_list = [

    ]
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

def w_k_regret_dlf():
    constraints_list = [

    ]
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


def w_k_regret_dlhf():
    constraints_list = [

    ]
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




def random_insertion():
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    return data
    
def random_insertion_dynamic():
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    return data

def random_insertion_dlf():
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    return data
    

def random_insertion_dlhf():
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


def first_insertion():
    data = {
            "obj_func_name" : "ObjDistancePDPTW",
            "constraints_names" : [
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ]
        }
    return data


def first_insertion_dynamic():
    data = first_insertion()
    data["constraints_name"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests"
    ]
    return data

def first_insertion_dlf():
    data = first_insertion_dynamic()
    data["constraints_name"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests"
    ]

    return data
    
def first_insertion_dlhf():
    data = first_insertion_dynamic()
    data["constraints_name"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "HeterogeneousFleet"
    ]

    return data
