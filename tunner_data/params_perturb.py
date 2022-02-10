
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
            "TimeWindowsConstraint"
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

def random_exchange():
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ]
    }
    
    return data