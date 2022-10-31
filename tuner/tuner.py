import multiprocessing
import os
import random
import subprocess
import sys
from click import argument
import hyperopt
import pprint
import json
import math
import numpy

sys.path.append('solver/')
sys.path.append('tuner/')


import solver

import best_configuration_maker

from tuner_src import params_constructives
from tuner_src import params_insertions
from tuner_src import params_removals
from tuner_src import params_perturb

from tuner_src import params_meta
from tuner_src import params_solver
from tuner_src import params_constraints
from tuner_src import params_objectives
from tuner_src import params_files_manager
from tuner_src import params_routes


big_m = 99999999999999999999999999999999999999
config_idx = 0
params_configs = {}
config_id_params = {}
results_configs = {}

params_dict = {}

log_file_name = None


def make_hyperopt_params_dict():
    importeds = [
        params_constructives,
        params_insertions,
        params_removals,
        params_perturb,
        params_meta,
        params_solver,
        params_constraints,
        params_objectives,
        params_files_manager,
        params_routes
    ]
    
    dict_params = {}
    for imported in importeds:
        params = imported.get_params_dict()
        for key, value in params.items():
            dict_params[key] = value

    return dict_params


def add_to_param_dict(param_label, param):
    global params_dict
    params_dict[param_label] = param


def read_command_line_inputs():
    arguments = sys.argv[1:]
    print(len(arguments))
    if (len(arguments) < 4):
        text = "\n"
        text += "COMMAND LINE ARGUMENTS:\n\n"
        text += "python3 tuner.py <inputs_list_file> <outputs_dir_path> "
        text += "<best_configuration_ouput_file> <time_limit>"
        text += "<number-of-evaluations>\n\n"
        text += "*Time limit = -1 will set the time as a parameter\n\n"
        text += "*Number of Evaluations is optional with 50 as default\n\n"
        print(text)
        exit(0)
    
    data = {}
    
    with open(arguments[0], "r") as input_list_f:
        inputs = input_list_f.read().strip().split("\n")

    data["inputs"] = inputs
    data["output_path"] = arguments[1]
    data["best_config_file_name"] = arguments[2]
    data["time_limit"] = int(arguments[3])


    if (data["output_path"][-1] != "/"):
        data["output_path"] = data["output_path"] + "/"
    
    if (not os.path.exists(data["output_path"])):
        os.makedirs(data["output_path"])

    suffix = data["best_config_file_name"].split(".")
    if (len(suffix) < 2 or suffix[-1] != "json"):
        data["best_config_file_name"] = data["best_config_file_name"] + ".json"
    
    data["n_evals"] = 50
    if (len(arguments) == 5):
        data["n_evals"] = int(arguments[4])
    
    all_solutions_path = (
        data["output_path"] 
        + str("all_solutions/")
    )

    data["best_params_file_name"] = "best_params.json"

    if (not os.path.exists(all_solutions_path)):
        os.mkdir(all_solutions_path)
    
    global log_file_name
    log_file_name = os.path.join(data["output_path"], "log_file")
    
    return data


def write_log(text):
    with open(log_file_name, "a") as out:
        out.write(text)


def constructive_algs(problem):
    if (problem == "PDPTW"):
        algs_data = {
            "BasicGreedy" : params_constructives.basic_greedy()
        }
    if (problem == "DPDPTW"):
        algs_data = {
            "BasicGreedy" : params_constructives.basic_greedy_dynamic()
        }
    if (problem == "DPDPTWNoC-D"):
        algs_data = {
            "BasicGreedyLimitedFleet" : (
                params_constructives.basic_greedy_dynamic_no_cap()
            )
        }
    if (problem == "DPDPTWLF-R"):
        algs_data = {
            "BasicGreedyLimitedFleet" : (
                params_constructives.basic_greedy_limited_fleet()
            )
        }
    if (problem == "DPDPTWLHF-R"):
        algs_data = {
            "BasicGreedyLimitedHeterogeneousFleet" : (
                params_constructives.basic_greedy_limited_heterogeneous_fleet()
            )
        }

    return algs_data


def reinsertion_algs(problem):
    k_regret_name = "KRegret"
    k_regret = None
    wk_regret_name = "WKRegret"
    wk_regret = None
    random_insertion_name = "RandomInsertion"
    random_insertion = None
    first_insertion_name = "FirstInsertion"
    first_insertion = None

    if (problem == "PDPTW"):
        k_regret = params_insertions.k_regret()
        wk_regret = params_insertions.w_k_regret()
        random_insertion = params_insertions.random_insertion()
        first_insertion = params_insertions.first_insertion()
    if (problem == "DPDPTW"):
        k_regret = params_insertions.k_regret_dynamic()
        wk_regret = params_insertions.w_k_regret_dynamic()
        random_insertion = params_insertions.random_insertion_dynamic()
        first_insertion = params_insertions.first_insertion_dynamic()
    if (problem == "DPDPTWNoC-D"):
        k_regret = params_insertions.k_regret_dynamic_no_cap()
        wk_regret = params_insertions.w_k_regret_dynamic_no_cap()
        random_insertion = params_insertions.random_insertion_dynamic_no_cap()
        first_insertion = params_insertions.first_insertion_dynamic_no_cap()
    if (problem == "DPDPTWLF-R"):
        k_regret = params_insertions.k_regret_dlf()
        wk_regret = params_insertions.w_k_regret_dlf()
        random_insertion = params_insertions.random_insertion_dlf()
        first_insertion = params_insertions.first_insertion_dlf()
    if (problem == "DPDPTWLHF-R"):
        k_regret = params_insertions.k_regret_dlhf()
        wk_regret = params_insertions.w_k_regret_dlhf()
        random_insertion = params_insertions.random_insertion_dlhf()
        first_insertion = params_insertions.first_insertion_dlhf()

    algs_data = {
        k_regret_name : k_regret,
        wk_regret_name : wk_regret,
        random_insertion_name : random_insertion,
        first_insertion_name : first_insertion
    }
    return algs_data


def removal_algs(problem):

    rr_name = None
    rr = None
    wr_name = None
    wr = None
    sr_name = None
    sr = None

    if (problem == "PDPTW"):
        rr_name = "RandomRemoval"
        rr = params_removals.random_removal()
        wr_name = "WorstRemoval"
        wr = params_removals.worst_removal()
        sr_name = "ShawRemovalPDPTW"
        sr = params_removals.shaw_removal_PDPTW()
    if (
        problem == "DPDPTW" 
        or problem == "DPDPTWLF-R"
        or problem == "DPDPTWLHF-R"
        or problem == "DPDPTWNoC-D"
    ):
        rr_name = "RandomRemoval"
        rr = params_removals.random_removal_dynamic()
        wr_name = "WorstRemoval"
        wr = params_removals.worst_removal_dynamic()
        sr_name = "ShawRemovalDPDPTW"
        sr = params_removals.shaw_removal_DPDPTW()
        

    algs_data = {
        rr_name : rr,
        wr_name : wr,
        sr_name : sr
    }
    return algs_data


def perturb_algs(problem):
    rs_name = "RandomShift"
    rs = None
    mbs_name = "ModBiasedShift"
    mbs = None
    re_name = "RandomExchange"
    re = None

    if (problem == "PDPTW"):
        rs = params_perturb.random_shift()
        mbs = params_perturb.mod_biased_shift()
        re = params_perturb.random_exchange()
    if (problem == "DPDPTW"):
        rs = params_perturb.random_shift_dynamic()
        mbs = params_perturb.mod_biased_shift_dynamic()
        re = params_perturb.random_exchange_dynamic()
    if (problem == "DPDPTWLF-R"):
        rs = params_perturb.random_shift_dlf()
        mbs = params_perturb.mod_biased_shift_dlf()
        re = params_perturb.random_exchange_dlf()
    if (problem == "DPDPTWLHF-R"):
        rs = params_perturb.random_shift_dlhf()
        mbs = params_perturb.mod_biased_shift_dlhf()
        re = params_perturb.random_exchange_dlhf()
    if (problem == "DPDPTWNoC-D"):
        rs = params_perturb.random_shift_dynamic_no_cap()
        mbs = params_perturb.mod_biased_shift_dynamic_no_cap()
        re = params_perturb.random_exchange_dynamic_no_cap()



    algs_data = {
        rs_name : rs,
        mbs_name : mbs,
        re_name : re
    }
    
    return algs_data


def meta_algs(problem, exclude_fop=False):

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
        fop = params_meta.ages()
        sop = params_meta.lns()
        exact_name = "SetPartitionModel"
        exact = params_meta.set_partitioning()
        perturb = params_meta.original_perturbation()
        sb = params_meta.sb_math()
    if (problem == "DPDPTW"):
        fop = params_meta.ages_dynamic()
        sop = params_meta.lns_dynamic()
        exact_name = "SetPartitionModel"
        exact = params_meta.set_partitioning_dynamic()
        perturb = params_meta.original_perturbation_dynamic()
        sb = params_meta.sb_math_dynamic()
    if (problem == "DPDPTWLF-R"):
        fop = params_meta.ages_dlf()
        sop = params_meta.lns_dlf()
        exact_name = "PartitionMaxRequests"
        exact = params_meta.partitioning_max_requests()
        perturb = params_meta.original_perturbation_dlf()
        sb = params_meta.sb_math_dlf()
    if (problem == "DPDPTWLHF-R"):
        fop = params_meta.ages_dlhf()
        sop = params_meta.lns_dlhf()
        exact_name = "PartitionMaxRequestsHF"
        exact = params_meta.partition_max_requests_hf()
        perturb = params_meta.original_perturbation_dlhf()
        sb = params_meta.sb_math_dlhf()
    if (problem == "DPDPTWNoC-D"):
        fop = params_meta.ages_dynamic_no_cap()
        sop = params_meta.lns_dynamic_no_cap()
        exact_name = "SetPartitionModel"
        exact = params_meta.set_partitioning_dynamic_no_cap()
        perturb = params_meta.original_perturbation_dynamic_no_cap()
        sb = params_meta.sb_math_dynamic_no_cap()

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



def solvers_algs(problem):
    if (problem == "PDPTW"):
        sol_algs = {
            "SolverPDPTW" : params_solver.solver_pdptw()
        }
    
    if (problem == "DPDPTW"):
        sol_algs = {
            "SolverDPDPTW" : params_solver.solver_dpdptw()
        }
    if (problem == "DPDPTWNoC-D"):
        sol_algs = {
            "SolverDPDPTW" : params_solver.solver_dpdptw_no_cap()
        }
    if (problem == "DPDPTWLF-R"):
        sol_algs = {
            "SolverDPDPTW" : params_solver.solver_pdptwlfr()
        }

    if (problem == "DPDPTWLHF-R"):
        sol_algs = {
            "SolverDPDPTWHeterogeneousFleet" : params_solver.solver_pdptwlhfr()
        }
    
    return sol_algs


def constraints_data(problem):
    constr_data = {}
    if (problem == "PDPTW"):
        constr_data = {
            "TimeWindowsConstraint" : (
                params_constraints.time_windows_constraint()
            ),
            "HomogeneousCapacityConstraint": (
                params_constraints.homogeneous_capacity_constraint()
            ),
            "PickupDeliveryConstraint": (
                params_constraints.pickup_delivery_constraint()
            ),
            "AttendAllRequests" : params_constraints.attend_all_requests()
        }
    if (problem == "DPDPTW"):
        constr_data = {
            "TimeWindowsConstraint" : (
                params_constraints.time_windows_constraint()
            ),
            "HomogeneousCapacityConstraint": (
                params_constraints.homogeneous_capacity_constraint()
            ),
            "PickupDeliveryConstraint": (
                params_constraints.pickup_delivery_constraint()
            ),
            "AttendAllRequests" : params_constraints.attend_all_requests(),

            "FixedRequests" : params_constraints.fixed_requests()
        }
    if (problem == "DPDPTWNoC-D"):
        constr_data = {
            "TimeWindowsConstraint" : (
                params_constraints.time_windows_constraint()
            ),
            "PickupDeliveryConstraint": (
                params_constraints.pickup_delivery_constraint()
            ),
            "AttendAllRequests" : params_constraints.attend_all_requests(),

            "FixedRequests" : params_constraints.fixed_requests(),

            "LimitedFleet" : params_constraints.limited_fleet()    
        }
    if (problem == "DPDPTWLF-R"):
        constr_data = {
            "TimeWindowsConstraint" : (
                params_constraints.time_windows_constraint()
            ),
            "HomogeneousCapacityConstraint": (
                params_constraints.homogeneous_capacity_constraint()
            ),
            "PickupDeliveryConstraint": (
                params_constraints.pickup_delivery_constraint()
            ),
            "AttendAllRequests" : params_constraints.attend_all_requests(),

            "FixedRequests" : params_constraints.fixed_requests(),

            "LimitedFleet" : params_constraints.limited_fleet()    
        }
    
    if (problem == "DPDPTWLHF-R"):

        constr_data = {
            "TimeWindowsConstraint" : (
                params_constraints.time_windows_constraint()
            ),
            "HomogeneousCapacityConstraint": (
                params_constraints.homogeneous_capacity_constraint()
            ),
            "PickupDeliveryConstraint": (
                params_constraints.pickup_delivery_constraint()
            ),
            "AttendAllRequests" : params_constraints.attend_all_requests(),

            "FixedRequests" : params_constraints.fixed_requests(),

            "LimitedFleet" : params_constraints.limited_fleet(),
            
            "HeterogeneousFleet" : params_constraints.heterogeneous_fleet()
        }
    
    return constr_data

def objectives_data():
    obj_data = {
        "ObjDistancePDPTW" : params_objectives.obj_distance_PDPTW(),
        "ObjVehiclePDPTW" : params_objectives.obj_vehicles(),
        "ObjRequestsPDPTW" : params_objectives.obj_requests_PDPTW()
    }
    
    return obj_data


def reader_data(problem):
    if (problem == "PDPTW"):
        reader_classes_data = {
            "ReaderJsonPDPTW" : params_files_manager.reader_json_PDPTW(),
        }
    if (problem == "DPDPTW"):
        reader_classes_data = {
            "ReaderJsonDPDPTW" : params_files_manager.reader_json_DPDPTW(),
        }
    if (problem == "DPDPTWLF-R" or problem == "DPDPTWNoC-D"):
        reader_classes_data = {
            "ReaderJsonDPDPTWLimitedFleet" : (
                params_files_manager.reader_json_DPDPTWLF()
            ),
        }
    if (problem == "DPDPTWLHF-R"):
        reader_classes_data = {
            "ReaderJsonDPDPTWLimitedHeterogeneousFleet" : (
                params_files_manager.reader_json_DPDPTWLHF()
            )
        }
    
    return reader_classes_data


def writer_data():
    writer_classes_data = {
        "WriterLiLimPDPTW" : params_files_manager.writer_li_lim_PDPTW()
    }
    
    return writer_classes_data


def route_data(problem):
    if (problem == "PDPTW"):
        r_data = {
            "RoutePDPTW" : params_routes.route_pdptw(),
        }
    if (
        problem == "DPDPTW" 
        or problem == "DPDPTWLF-R" 
        or problem == "DPDPTWNoC-D"
    ):

        r_data = {
            "RouteDPDPTW" : params_routes.route_dpdptw(),
        }
    if (problem == "DPDPTWLHF-R"):
        r_data = {
            "RouteDPDPTWHeterogeneousFleet" : params_routes.route_dpdptwlhf()
        }

    return r_data


def vertex_data(problem):
    if (problem == "PDPTW"):
        v_data = {
            "VertexPDPTW" : params_routes.vertex_pdptw(),
        }
    if (
        problem == "DPDPTW" 
        or problem == "DPDPTWLF-R" 
        or problem == "DPDPTWNoC-D"
    ):
        v_data = {
            "VertexDPDPTW" : params_routes.vertex_dpdptw(),
        }
    if (problem == "DPDPTWLHF-R"):
        v_data = {
            "VertexDPDPTWHeterogeneousFleet" : (
                params_routes.vertex_dpdptwlhf()
            )
        }

    return v_data


def insertion_operator_data():
    if (problem == "PDPTW"):
        insert_data = {
            "InsertionOperatorPDPTW" : params_routes.insertion_operator_pdptw()
        }
    if (
        problem == "DPDPTW" 
        or problem == "DPDPTWLF-R" 
        or problem == "DPDPTWLHF-R"
    ):
        insert_data = {
            "InsertionOperatorDPDPTW" : (
                params_routes.insertion_operator_dpdptw()
            )
        }
    if (problem == "DPDPTWNoC-D"):
        insert_data = {
            "InsertionOperatorDPDPTWNoCap" : (
                params_routes.insertion_operator_dpdptw_no_cap()
            )
        }
    return insert_data


def removal_operator_data():
    if (problem == "PDPTW"):
        remov_data = {
            "RemovalOperatorPDPTW" : params_routes.removal_operator_pdptw()
        }
    if (
        problem == "DPDPTW" 
        or problem == "DPDPTWLF-R" 
        or problem == "DPDPTWLHF-R"
    ):
        remov_data = {
            "RemovalOperatorPDPTW" : params_routes.removal_operator_dpdptw()
        }
    if (problem == "DPDPTWNoC-D"):
        remov_data = {
            "RemovalOperatorDPDPTWNoCap" : (
                params_routes.removal_operator_dpdptw_no_cap()
            )
        }
    return remov_data


def make_configuration_input_file(configuration, config_file_name):
    algs_keys = [
        "constructive_algs",
        "reinsertion_algs",
        "removal_algs",
        "perturb_algs",
        "meta_algs"
    ]
    
    reader_class_name = list(configuration["reader"].keys())[0]
    wirter_class_name = list(configuration["writer"].keys())[0]
    
    route_class_name = list(configuration["route"].keys())[0]
    vertex_class_name = list(configuration["vertex"].keys())[0]
    
    insertion_class_name = list(configuration["insertion"].keys())[0]
    removal_class_name = list(configuration["removal_operator"].keys())[0]
    
    out_data = {}
    
    out_data["objective"] = configuration["objectives"]
    out_data["constraints"] = configuration["constraints"]
    
    out_data["reader"] = {
        reader_class_name : configuration["reader"][reader_class_name]
    }
    
    out_data["writer"] = {
        wirter_class_name : configuration["writer"][wirter_class_name]
    }
    
    out_data["route_class"] = {
        route_class_name : configuration["route"][route_class_name]
    }
    
    out_data["vertex_class"] = {
        vertex_class_name : configuration["vertex"][vertex_class_name]
    }
    
    out_data["insertion_operator"] = {
        insertion_class_name : (
            configuration["insertion"][insertion_class_name]
        )
    }
    
    out_data["removal_operator"] = {
        removal_class_name : (
            configuration["removal_operator"][removal_class_name]
        )
    }
    
    out_data["solution_methods"] = {}

    
    for algs_key in algs_keys:
        for name, algorithm in configuration[algs_key].items():
            out_data["solution_methods"][name] = algorithm

    solver_name = configuration["solver"]
    out_data["solver"] = {
        solver_name : configuration["solvers_algs"][solver_name]
    }
    data = json.dumps(out_data, indent=4)
    
    with open(config_file_name, "w+") as f:
        f.write(data)


def execute(arguments, results=None, result_pos=None):
    
    solver_path = "./solver/solver.py"
    
    input_path = arguments["input"]
    output = arguments["output"]
    config_file = arguments["configuration_file"]
    time_limit = arguments["time_limit"]
    seed = arguments["seed"]

    command = ""
    command += str(sys.executable) + " "
    command += solver_path + " "
    command += "--input" + " " + str(input_path) + " "
    command += "--output" + " " + str(output) + " "
    command += "--set-config-file" + " " + str(config_file) + " "
    command += "--set-time-limit" + " " + str(time_limit) + " "
    command += "--set-seed" + " " + str(seed) + " "
    command += "--make-log" + " "
    command += "--detail-solution-log" + " "
    print("-----")
    print("running: ", result_pos)
    print(command)
    print("-----")

    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    sp_output = sp.communicate(timeout=time_limit+5)[0]
    # exit_code = sp.returncode
    # for line in sp_output.splitlines():
    #     print(line.decode("utf-8"))
    # print(exit_code)

    o_name = os.path.basename(output)
    o_name = o_name.split(".")[0] + "_sol_data.json"
    o_name = os.path.join(arguments["output_path"], o_name)

    with open(o_name, "r") as out_sol:
        results[result_pos] = json.loads(out_sol.read())
        
    return results[result_pos]


def solve_inputs(inputs, output_path, time_limit, config_file):
    global config_idx
    
    manager = multiprocessing.Manager()
    results = manager.dict()

    chunk_size = 2
    process_list = []
    i = 0
    while (i < len(inputs)):
        arguments = {}
        
        arguments["output_path"] = os.path.join(output_path, "all_solutions")
        
        output = "".join(inputs[i].split("/")[-1].split(".")[0])
        output += "_config_" + str(config_idx) + ".txt"
        output = os.path.join(arguments["output_path"], output)
        
        arguments["configuration_file"] = config_file
        arguments["seed"] = random.randint(0, 10000000)
        arguments["time_limit"] = time_limit
        arguments["make_log"] = True
        arguments["detail_sol"] = True
        arguments["input"] = inputs[i]
        arguments["output"] = output
        

        # result = solver.execute(arguments=arguments)
        # results[i] = result
        
        p = multiprocessing.Process(
            target=execute, 
            args=(arguments, results, i)
        )
        process_list.append(p)
        p.start()
        i += 1
        
        if (len(process_list) >= chunk_size):
            for p in process_list:
                p.join()
                process_list = []
        

    for p in process_list:
        p.join()

    # for result in results.values():
    #     print(result)


    return results


def read_cost_matrix_dict(input_name):
    with open(input_name, "r") as inp:
        text = inp.read()
        dict_data = json.loads(text)
        dict_matrix = dict_data["distance_matrix"]
        return dict_matrix


def get_routes_upper_bound(number_of_routes, matrix_dict):
    matrix_arr = numpy.array([
        list(matrix_dict[i].values()) for i in matrix_dict.keys()
    ])
    
    lines_maxes = numpy.amax(matrix_arr, 1)
    
    concat_matrix = numpy.concatenate(tuple((line for line in matrix_arr)))
    partitioned = -numpy.partition(-concat_matrix, number_of_routes+1)
    matrix_maxes = partitioned[:number_of_routes+1]

    maxes = numpy.concatenate((lines_maxes, matrix_maxes))

    return sum(maxes)



def calculate_solution_value(results, norm_divisor):

    instances_upper_costs = {}
    for i, result in results.items():
        if (result["solution"] is None):
            continue
        inp = inputs[i]
        matrix_dict = read_cost_matrix_dict(inp)
        routes_num = len(result["solution"]["routes"])
        matrix_upper_bound = get_routes_upper_bound(routes_num, matrix_dict)
        instances_upper_costs[i] = matrix_upper_bound
    
    norm_routes_cost = {}
    for i, result in results.items():
        if (result["solution"] is None):
            continue
        routes_costs = result["solution"]["solution_routes_cost"]
        upper_cost = instances_upper_costs[i]
        norm_routes_cost[i] = (routes_costs / upper_cost) / norm_divisor
    
    solution_costs = sum([
        results[i]["solution"]["solution_cost"] + norm_route_cost
        for i, norm_route_cost in norm_routes_cost.items()
    ])
    print(solution_costs)
    
    for result in results.values():
        if (result["solution"] is None):
            solution_costs += big_m
    
    return solution_costs


def get_obj(params):
    global config_idx
    config_idx += 1
    
    configuration, inputs, output_path, time_limit, h_opt_dict = params
    
    if (time_limit == -1):
        time_limit = configuration["time"]
    print("time limit:", time_limit)
    
    global config_id_params
    config_id_params[config_idx] = configuration
    
    params_tuple = tuple(sorted(h_opt_dict.items()))
    
    global params_configs
    params_configs[params_tuple] = configuration
    
    config_file = output_path + "configuration_" + str(config_idx) + ".json"
    
    make_configuration_input_file(configuration, config_file)
    
    results = solve_inputs(inputs, output_path, time_limit, config_file)

    normalized_cost_divisor = 10 ** (int(math.log(len(inputs), 10)) + 1)
    
    fo = calculate_solution_value(results, normalized_cost_divisor)
    
    print("\n\nEval result: " + str(fo) + "\n\n")
    
    global results_configs
    results_configs[config_idx] = fo

    return fo



if __name__ == "__main__":
    # print(getattr("solver","solver"))

    command_input_data = read_command_line_inputs()

    # problem = "PDPTW"
    # problem = "DPDPTW"
    # problem = "DPDPTWLF-R"
    # problem = "DPDPTWLHF-R"
    problem = "DPDPTWNoC-D"
    exclude_fop = True

    random.seed(0)
    print("STARTING SEED", 0)
    configuration = {
        "solver" : params_solver.solvers_options(problem),
        "solvers_algs" : solvers_algs(problem),

        "constructive_algs" : constructive_algs(problem),
        "reinsertion_algs" : reinsertion_algs(problem),
        "removal_algs" : removal_algs(problem),
        "perturb_algs" : perturb_algs(problem),
        "meta_algs" : meta_algs(problem, exclude_fop),

        "constraints" : constraints_data(problem),
        "objectives" : objectives_data(),

        "writer" : writer_data(),
        "reader" : reader_data(problem),

        "insertion" : insertion_operator_data(),
        "removal_operator" : removal_operator_data(),

        "route" : route_data(problem),
        "vertex" : vertex_data(problem),

        "time" : hyperopt.hp.choice("time_limit_sb", [300, 480, 600])
        # "time" : hyperopt.hp.choice("time_limit_sb", [10, 20, 30])
    }

    inputs = command_input_data["inputs"]
    params = (
        configuration, 
        inputs, 
        command_input_data["output_path"],
        command_input_data["time_limit"],
        make_hyperopt_params_dict()
    )
    print("Calling fmin")
    best_params = hyperopt.fmin(
        fn=get_obj, 
        space=params, 
        algo=hyperopt.tpe.suggest, 
        max_evals=command_input_data["n_evals"]
    )
    
    
    params_converted = {}
    for key, value in best_params.items():
        if isinstance(value, numpy.integer):
            params_converted[key] = int(value)
        if isinstance(value, numpy.floating):
            params_converted[key] = float(value)
        if isinstance(value, numpy.ndarray):
            params_converted[key] = value.tolist()



    best_params_file = os.path.join(
        command_input_data["output_path"], 
        "best_params.json"
    )

    with open(best_params_file, "w+") as best_file:
        best_file.write(json.dumps(params_converted, indent=2))
    
    out_data = best_configuration_maker.get_configuration_dict(
        params_converted, 
        problem,
        exclude_fop
    )


    best_out = (
        command_input_data["output_path"] 
        + command_input_data["best_config_file_name"]
    )
    

    # WRITE BEST CONFIG FILE
    with open(best_out, "w") as best_file:
        best_file.write(json.dumps(out_data, indent=4))
    
        
    