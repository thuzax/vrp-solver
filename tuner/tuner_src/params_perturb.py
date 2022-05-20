
import hyperopt


perturb_params = {}


def get_params_dict():
    global perturb_params
    return perturb_params


def perturb_options():
    choice = hyperopt.hp.choice(
        "perturb_opt",
        [("RandomShift", "ModBiasedShift", "RandomExchange")]
    )
    
    global perturb_params
    perturb_params["perturb_opt"] =  choice
    
    return choice


def random_shift():
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
        ]
    }
    
    return data

def random_shift_dynamic():
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    
    return data

def random_shift_dlf():
    data = {
        "obj_func_name" : "ObjRequestsPDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests",
            "LimitedFleet"
        ]
    }
    
    return data

def random_shift_dlhf():
    data = {
        "obj_func_name" : "ObjRequestsPDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests",
            "LimitedFleet",
            "HeterogeneousFleet"
        ]
    }
    
    return data

def mod_biased_shift():
    mi = hyperopt.hp.uniform("mi_prob", 1, 10)
    
    global perturb_params
    perturb_params["mi_prob"] = mi
    
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ],
        "mi" : mi
    }
    
    return data

def mod_biased_shift_dynamic():
    data = mod_biased_shift()
    
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
    ]
        
    return data

def mod_biased_shift_dlf():
    data = mod_biased_shift_dynamic()
    
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]

    data["obj_func_name"] = "ObjRequestsPDPTW"
    
    return data
    

def mod_biased_shift_dlhf():
    data = mod_biased_shift_dlf()
    
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]
    
    return data

def random_exchange():
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    
    return data

def random_exchange_dynamic():
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    
    return data

def random_exchange_dlf():
    data = {
        "obj_func_name" : "ObjRequestsPDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests",
            "LimitedFleet"
        ]
    }
    
    return data

def random_exchange_dlhf():
    data = {
        "obj_func_name" : "ObjRequestsPDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests",
            "LimitedFleet",
            "HeterogeneousFleet"
        ]
    }
    
    return data