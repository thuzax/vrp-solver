
perturb_params = {}

def perturb_options(params):
    opts = [("RandomShift", "ModBiasedShift", "RandomExchange")]
    choice = opts[params["perturb_opt"]]
    return choice


def random_shift(params):
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
        ]
    }
    
    return data

def random_shift_dynamic(params):
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    
    return data

def random_shift_dlf(params):
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

def random_shift_dlhf(params):
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

def mod_biased_shift(params):
    mi = params["mi_prob"]
    
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

def mod_biased_shift_dynamic(params):
    data = mod_biased_shift(params)
    
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
    ]
        
    return data

def mod_biased_shift_dlf(params):
    data = mod_biased_shift_dynamic(params)
    
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]

    data["obj_func_name"] = "ObjRequestsPDPTW"
    
    return data
    

def mod_biased_shift_dlhf(params):
    data = mod_biased_shift_dlf(params)
    
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]
    
    return data

def random_exchange(params):
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    
    return data

def random_exchange_dynamic(params):
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests"
        ]
    }
    
    return data

def random_exchange_dlf(params):
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

def random_exchange_dlhf(params):
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


def perturb_data(params, problem):
    rs_name = "RandomShift"
    rs = None
    mbs_name = "ModBiasedShift"
    mbs = None
    re_name = "RandomExchange"
    re = None

    if (problem == "PDPTW"):
        rs = random_shift(params)
        mbs = mod_biased_shift(params)
        re = random_exchange(params)
    if (problem == "DPDPTW"):
        rs = random_shift_dynamic(params)
        mbs = mod_biased_shift_dynamic(params)
        re = random_exchange_dynamic(params)
    if (problem == "DPDPTWLF-R"):
        rs = random_shift_dlf(params)
        mbs = mod_biased_shift_dlf(params)
        re = random_exchange_dlf(params)
    if (problem == "DPDPTWLHF-R"):
        rs = random_shift_dlhf(params)
        mbs = mod_biased_shift_dlhf(params)
        re = random_exchange_dlhf(params)



    algs_data = {
        rs_name : rs,
        mbs_name : mbs,
        re_name : re
    }
    
    return algs_data