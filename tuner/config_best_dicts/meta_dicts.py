from config_best_dicts import insertions_dicts

meta_params = {}

def meta_options(params):
    opts = [
        ("AGES", "LNS", "SetPartitionModel", "OriginalPerturbation", "SBMath")
    ]
    meta_choice = opts[params["metaheuristic"]]
    meta_params["metaheuristic"] = meta_choice
    return meta_choice


def ages(params):
    max_number_of_perturbations =  params["max_pert"]     
    number_of_perturb_moves = params["n_pert"]
    
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

def ages_dynamic(params):
    data = ages(params)
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    return data

def ages_dynamic_no_cap(params):
    data = ages_dynamic(params)
    data["constraints_names"] =  [
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data


def ages_dlf(params):
    data = ages(params)
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjVehiclePDPTW"

    return data

def ages_dlhf(params):
    data = ages(params)
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]
    data["obj_func_name"] = "ObjVehiclePDPTW"

    return data


def lns(params):
    max_it = params["max_it"]
    max_it_improv = params["max_it_improv"]
    k_min = params["k_min"]
    k_max = params["k_max"]
    b_min = params["b_min"]
    b_max = params["b_max"]

    rr_prob = params["rr_prob"]
    wr_prob = params["wr_prob"]
    sr_prob = params["sr_prob"]
    
    size = params["size"]
    
    global meta_params
    
    meta_params["max_it_improv"] = max_it_improv
    meta_params["k_min"] = k_min
    meta_params["k_max"] = k_max
    meta_params["b_min"] = b_min
    meta_params["b_max"] = b_max
    meta_params["rr_prob"] = rr_prob
    meta_params["wr_prob"] = wr_prob
    meta_params["sr_prob"] = sr_prob
    meta_params["size"] = size
    
    
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "AttendAllRequests"
        ],
        "acceptance_algorithm_data" : {
            "LAHC" : {
                "list_size" : size
            }
        },
        "local_operators_names" : {
            "KRegret" : insertions_dicts.reinsertion_options(params),
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

def lns_dynamic(params):
    data = lns(params)
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    data["local_operators_names"]["ShawRemoval"] = "ShawRemovalDPDPTW"

    return data


def lns_dynamic_no_cap(params):
    data = lns_dynamic(params)
    data["constraints_names"] =  [
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data


def lns_dlf(params):
    data = lns_dynamic(params)
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]

    data["obj_func_name"] = "ObjRequestsPDPTW"

    return data

def lns_dlhf(params):
    data = lns_dlf(params)
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]

    return data



def set_partitioning(params):
    data = {
        "obj_func_name" : "ObjVehiclePDPTW",
        "constraints_names" : [
            "AttendAllRequests",
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint"
        ],
        "solver_code" : "GRB",
        "opt_time_limit" : int(120)
    }
    
    return data


def set_partitioning_dynamic(params):
    data = set_partitioning(params)
    data["constraints_names"] =  [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    return data

def set_partitioning_dynamic_no_cap(params):
    data = set_partitioning_dynamic(params)
    data["constraints_names"] =  [
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data


def partitioning_max_requests(params):
    data = {
        "obj_func_name" : "ObjRequestsPDPTW",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "FixedRequests",
            "LimitedFleet"
        ],
        "solver_code" : "GRB",
        "opt_time_limit" : int(120),
        "max_routes_cost_increment" : params["mrc_incr"],
        "cost_reduction_factor" : float(0.000001)
    }
    
    return data

def partition_max_requests_hf(params):
    data = partitioning_max_requests(params)
    data["constraints"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]

    return data



def original_perturbation(params): 
    rs_prb = params["rs_prb"]
    re_prb = params["re_prb"]
    bs_prb = params["bs_prb"]
    
    
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


def original_perturbation_dynamic(params):
    data = original_perturbation(params)
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    return data


def original_perturbation_dynamic_no_cap(params):
    data = original_perturbation_dynamic(params)
    data["constraints_names"] =  [
        "TimeWindowsConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data




def original_perturbation_dlf(params):
    data = original_perturbation(params)
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjRequestsPDPTW"

    return data


def original_perturbation_dlhf(params):
    data = original_perturbation_dlf(params)
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "FixedRequests",
        "LimitedFleet",
        "HeterogeneousFleet"
    ]
    return data



def sb_math(params): 
    global meta_params
    meta_params["max_pert_math"] = params["max_pert_math"]
    
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
        "max_time" : int(10000000000),
        "max_it" : int(10000000),
        "max_it_without_improv" : int(300000),
        "acceptance_algorithm_data" : {
            "AcceptBetterOrWithProbability" : {}
        },
        "routes_diff_method" : "set",
        "number_of_perturb_moves" : meta_params["max_pert_math"]
    }
    return data


def sb_math_dynamic(params): 
    data = sb_math(params)
    data["constraints_names"] = [
        "HomogeneousCapacityConstraint",
        "TimeWindowsConstraint",
        "PickupDeliveryConstraint",
        "FixedRequests",
        "AttendAllRequests"
    ]

    return data

def sb_math_dynamic_no_cap(params): 
    data = sb_math_dynamic(params)
    data["constraints_names"] = [
        "TimeWindowsConstraint",
        "PickupDeliveryConstraint",
        "FixedRequests",
        "AttendAllRequests",
        "LimitedFleet"
    ]
    data["obj_func_name"] = "ObjDistancePDPTW"

    return data




def sb_math_dlf(params): 
    data = sb_math(params)
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


def sb_math_dlhf(params):
    data = sb_math_dlf(params)
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

def meta_algs_data(params, problem, exclude_fop=False):

    fop_name = "AGES"
    fop = None
    sop_name = "LNS"
    sop = None
    exact_name = None
    exact = None
    perturb_name = "OriginalPerturbation"
    perturb = None
    sb_name = "SBMath"
    sb = None

    if (problem == "PDPTW"):
        fop = ages(params)
        sop = lns(params)
        exact_name = "SetPartitionModel"
        exact = set_partitioning(params)
        perturb = original_perturbation(params)
        sb = sb_math(params)
    if (problem == "DPDPTW"):
        fop = ages_dynamic(params)
        sop = lns_dynamic(params)
        exact_name = "SetPartitionModel"
        exact = set_partitioning_dynamic(params)
        perturb = original_perturbation_dynamic(params)
        sb = sb_math_dynamic(params)
    if (problem == "DPDPTWNoC-D"):
        fop = ages_dynamic_no_cap(params)
        sop = lns_dynamic_no_cap(params)
        exact_name = "SetPartitionModel"
        exact = set_partitioning_dynamic_no_cap(params)
        perturb = original_perturbation_dynamic_no_cap(params)
        sb = sb_math_dynamic_no_cap(params)
    if (problem == "DPDPTWLF-R"):
        fop = ages_dlf(params)
        sop = lns_dlf(params)
        exact_name = "PartitionMaxRequests"
        exact = partitioning_max_requests(params)
        perturb = original_perturbation_dlf(params)
        sb = sb_math_dlf(params)
    if (problem == "DPDPTWLHF-R"):
        fop = ages_dlhf(params)
        sop = lns_dlhf(params)
        exact_name = "PartitionMaxRequestsHF"
        exact = partition_max_requests_hf(params)
        perturb = original_perturbation_dlhf(params)
        sb = sb_math_dlhf(params)

    if (exclude_fop):
        sb["excluded_local_operators"] = ["FirstOperator"]


    algs_data = {
        fop_name : fop,
        sop_name : sop,
        exact_name : exact,
        perturb_name : perturb,
        sb_name : sb
    }

    return algs_data