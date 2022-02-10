import hyperopt
from tunner_data import params_insertions

meta_params = {}


def get_params_dict():
    global meta_params
    return meta_params

def meta_options():
    meta_choice = hyperopt.hp.choice(
        "metaheuristic",
        [
            "AGES"
            "LNS"
            "SetPartitionModel"
            "OriginalPerturbation"
            "SBMath"
        ]
    )
    
    meta_params["metaheuristic"] = meta_choice
    
    return meta_choice


def ages():
    max_number_of_perturbations =  (
        hyperopt.hp.choice(
            "max_pert", 
            [i for i in range(1, 51)]
        )
    )
    
    number_of_perturb_moves = (
        hyperopt.hp.choice(
            "n_pert", 
            [i for i in range(1, 101)]
        )
    )
    
    global meta_params
    meta_params["max_pert"] = max_number_of_perturbations
    meta_params["n_pert"] =  number_of_perturb_moves
    
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
            "constraints_names" : [
                "AttendAllRequests",
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ],
            "acceptance_algorithm_data" : {
                "AcceptAll" : {}
            },
            "local_operators_names" : {
                "OriginalPerturbation" : "OriginalPerturbation"
            },
            "max_ejections" : 2,
            "stop_criteria" : "max_perturbation",
            "max_number_of_perturbations" : max_number_of_perturbations,
            "number_of_perturb_moves" : number_of_perturb_moves
            
    }
    
    return data

def lns():
    max_it = hyperopt.hp.choice(
        "max_it", 
        [i for i in range(100, 501)]
    )
    k_min = hyperopt.hp.choice(
        "k_min",
        [i for i in range(1, 7)]
    )
    k_max = hyperopt.hp.choice(
        "k_max",
        [i for i in range(1, 7)]
    )
    b_min = hyperopt.hp.choice(
        "b_min", 
        [i for i in range(1,6)]
    )
    b_max = hyperopt.hp.uniform("b_max", 0.1, 0.4)

    rr_prob = hyperopt.hp.uniform("rr_prob", 1, 10)
    wr_prob = hyperopt.hp.uniform("wr_prob", 1, 10)
    sr_prob = hyperopt.hp.uniform("sr_prob", 1, 10)
    
    
    global meta_params
    
    meta_params["max_it"] = max_it
    meta_params["k_min"] = k_min
    meta_params["k_max"] = k_max
    meta_params["b_min"] = b_min
    meta_params["b_max"] = b_max
    meta_params["rr_prob"] = rr_prob
    meta_params["wr_prob"] = wr_prob
    meta_params["sr_prob"] = sr_prob
    
    
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "AttendAllRequests"
        ],
        "acceptance_algorithm_data" : {
            "LAHC" : {
                "list_size" : (
                    hyperopt.hp.choice(
                        "size", 
                        [i for i in range(100, 200)]
                    )
                )
            }
        },
        "local_operators_names" : {
            "KRegret" : params_insertions.reinsertion_options(),
            "RandomRemoval" : "RandomRemoval",
            "WorstRemoval" : "WorstRemoval",
            "ShawRemoval" : "ShawRemovalPDPTW"
        },
        "stop_criteria" : "iterations",
        "max_time" : None,
        "max_time_without_improv" : None,
        "max_it" : 1001,
        "max_it_without_improv" : max_it,
        "k_min" : k_min,
        "k_max" : k_max,
        "b_min" : b_min,
        "b_max" : b_max,
        "removals_probabilities" : {
            "RandomRemoval" :rr_prob,
            "WorstRemoval" : wr_prob,
            "ShawRemoval" : sr_prob
        }
    }
    return data

def set_partitioning():
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "AttendAllRequests",
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ],
        "solver_code" : "CBC",
        "opt_time_limit" : 60
    }
    
    return data

def original_perturbation(): 
    rs_prb = hyperopt.hp.uniform("rs_prb", 1, 10)
    re_prb = hyperopt.hp.uniform("re_prb", 1, 10)
    bs_prb = hyperopt.hp.uniform("bs_prb", 1, 10)
    
    
    global meta_params
    meta_params["rs_prb"] = rs_prb
    meta_params["re_prb"] = re_prb
    meta_params["bs_prb"] = bs_prb
    
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ],
        "acceptance_algorithm_data" : {
            "AcceptAll" : {}
        },
        "local_operators_names" : {
            "RandomShift" : "RandomShift",
            "ModBiasedShift" : "ModBiasedShift",
            "RandomExchange" : "RandomExchange"
        },
        "perturb_probabilities" : {
            "RandomShift" : rs_prb,
            "RandomExchange" : re_prb,
            "ModBiasedShift" : bs_prb
        }
    }
    
    return data

def sb_math(): 
    global meta_params
    meta_params["max_pert_math"] = hyperopt.hp.choice(
        "max_pert_math", 
        [i for i in range(1, 301)]
    )
    
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "PickupDeliveryConstraint",
            "AttendAllRequests"
        ],
        "local_operators_names" : {
            "AGES" : "AGES",
            "LNS" : "LNS",
            "SetPartitionModel" : "SetPartitionModel",
            "OriginalPerturbation" : "OriginalPerturbation"
        },
        "excluded_local_operators" : [
        ],
        "stop_criteria" : "iterations",
        "max_time" : 0,
        "max_it" : 1000,
        "max_it_without_improv" : 300,
        "acceptance_algorithm_data" : {
            "AcceptBetterOrWithProbability" : {}
        },
        "routes_diff_method" : "set",
        "number_of_perturb_moves" : meta_params["max_pert_math"]
    }
    return data
