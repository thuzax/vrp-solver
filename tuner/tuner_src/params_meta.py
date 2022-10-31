import hyperopt
from tuner_src import params_insertions

meta_params = {}


def get_params_dict():
    global meta_params
    return meta_params

def meta_options():
    meta_choice = hyperopt.hp.choice(
        "metaheuristic",
        [("AGES", "LNS", "SetPartitionModel", "OriginalPerturbation", "SBMath")]
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
            [i for i in range(1, 51)]
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
            "Perturbation" : "OriginalPerturbation"
        },
        "max_ejections" : 2,
        "stop_criteria" : "max_perturbation",
        "max_number_of_perturbations" : max_number_of_perturbations,
        "number_of_perturb_moves" : number_of_perturb_moves
            
    }
    
    return data

def ages_dynamic():
    data = ages()
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    return data


def ages_dynamic_no_cap():
    data = ages_dynamic()
    data["constraints_names"] =  [
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data



def ages_dlf():
    data = ages()
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjVehiclePDPTW"

    return data

def ages_dlhf():
    data = ages()
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]
    data["obj_func_name"] = "ObjVehiclePDPTW"

    return data


def lns():
    max_it = hyperopt.hp.choice(
        "max_it", 
        [i for i in range(50, 301)]
    )
    max_it_improv = hyperopt.hp.choice(
        "max_it_improv", 
        [i for i in range(50, 201)]
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
    
    meta_params["max_it_improv"] = max_it_improv
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
                        [i for i in range(20, 150)]
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
        "max_it" : max_it,
        "max_it_without_improv" : max_it_improv,
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

def lns_dynamic():
    data = lns()
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    data["local_operators_names"]["ShawRemoval"] = "ShawRemovalDPDPTW"

    return data

def lns_dynamic_no_cap():
    data = lns_dynamic()
    data["constraints_names"] =  [
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data



def lns_dlf():
    data = lns_dynamic()
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]

    data["obj_func_name"] = "ObjRequestsPDPTW"

    return data

def lns_dlhf():
    data = lns_dlf()
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]

    return data



def set_partitioning():
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "AttendAllRequests",
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ],
        "solver_code" : "GRB",
        "opt_time_limit" : 120
    }
    
    return data


def set_partitioning_dynamic():
    data = set_partitioning()
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    return data

def set_partitioning_dynamic_no_cap():
    data = set_partitioning()
    data["constraints_names"] =  [
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data

def partitioning_max_requests():
    data = {
        "obj_func_name" : "ObjRequestsPDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests",
            "LimitedFleet"
        ],
        "solver_code" : "GRB",
        "opt_time_limit" : 120,
        "max_routes_cost_increment" : hyperopt.hp.uniform("mrc_incr", 0, 1),
        "cost_reduction_factor" : 0.000001
    }
    
    return data

def partition_max_requests_hf():
    data = partitioning_max_requests()
    data["constraints"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]

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


def original_perturbation_dynamic():
    data = original_perturbation()
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    return data

def original_perturbation_dynamic_no_cap():
    data = original_perturbation_dynamic()
    data["constraints_names"] =  [
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data

def original_perturbation_dlf():
    data = original_perturbation()
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjRequestsPDPTW"

    return data


def original_perturbation_dlhf():
    data = original_perturbation_dlf()
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]
    return data



def sb_math(): 
    global meta_params
    meta_params["max_pert_math"] = hyperopt.hp.choice(
        "max_pert_math", 
        [i for i in range(1, 51)]
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
            "FirstOperator" : "AGES",
            "SecondOperator" : "LNS",
            "ExactSolver" : "SetPartitionModel",
            "Perturbation" : "OriginalPerturbation"
        },
        "excluded_local_operators" : [
        ],
        "stop_criteria" : "time",
        "max_time" : 10000000000,
        "max_it" : 10000000,
        "max_it_without_improv" : 300000,
        "acceptance_algorithm_data" : {
            "AcceptBetterOrWithProbability" : {}
        },
        "routes_diff_method" : "set",
        "number_of_perturb_moves" : meta_params["max_pert_math"]
    }
    return data


def sb_math_dynamic(): 
    data = sb_math()
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "PickupDeliveryConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    return data

def sb_math_dynamic_no_cap(): 
    data = sb_math_dynamic()
    data["constraints_names"] = [
        "TimeWindowsConstraint",
        "PickupDeliveryConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data


def sb_math_dlf(): 
    data = sb_math()
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "PickupDeliveryConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]

    data["obj_func_name"] = "ObjRequestsPDPTW"
    data["local_operators_names"]["ExactSolver"] = "PartitionMaxRequests"
    data["excluded_local_operators"] = ["FirstOperator"]

    return data


def sb_math_dlhf():
    data = sb_math_dlf()
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "PickupDeliveryConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]

    data["local_operators_names"]["ExactSolver"] = "PartitionMaxRequestsHF"

    return data