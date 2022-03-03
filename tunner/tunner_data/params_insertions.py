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

def w_k_regret():
    data = {
        "non_insertion_cost" : 9999999999999,
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
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
    
