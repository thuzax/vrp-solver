import os
import random
import sys
import hyperopt
import pprint
import json
import math
import numpy

import solver

from tunner_data import params_constructives
from tunner_data import params_insertions
from tunner_data import params_removals
from tunner_data import params_perturb
from tunner_data import params_meta
from tunner_data import params_solver
from tunner_data import params_constraints
from tunner_data import params_objectives
from tunner_data import params_files_manager
from tunner_data import params_routes


big_m = 99999999999999999999999999999999999999
config_idx = 0
params_configs = {}
config_id_params = {}
results_configs = {}

params_dict = {}


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
    if (len(arguments) < 4):
        text = "\n"
        text += "COMMAND LINE ARGUMENTS:\n\n"
        text += "python3 tunner.py <inputs_list_file> <outputs_dir_path> "
        text += "<best_configuration_ouput_file> <time_limit>"
        text += "<number-of-evaluations>\n\n"
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
    
    suffix = data["best_config_file_name"].split(".")
    if (len(suffix) < 2 or suffix != "json"):
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
    
    return data




def constructive_algs():
    algs_data = {
        "BasicGreedy" : params_constructives.basic_greedy()
    }

    return algs_data


# def constructive_options():
#     choice = hyperopt.hp.choice(
#         "constructive_opt",
#         ["BasicGreedy", "WBasicGreedy"]
#     )
    
#     add_to_param_dict("constructive_opt", choice)

#     return choice


def reinsertion_algs():
    algs_data = {
        "KRegret" : params_insertions.k_regret(),
        "WKRegret" : params_insertions.w_k_regret(),
        "RandomInsertion" : params_insertions.random_insertion()
    }
    return algs_data


# def reinsertion_options():
#     choice = hyperopt.hp.choice(
#         "reinsertion_opt",
#         ["KRegret", "WKRegret"]
#     )
    
#     add_to_param_dict("reinsertion_opt", choice)
    
#     return choice


def removal_algs():
    algs_data = {
        "RandomRemoval" : params_removals.random_removal(),
        "WorstRemoval" : params_removals.worst_removal(),
        "ShawRemovalPDPTW" : params_removals.shaw_removal_PDPTW()
    }
    return algs_data


# def removal_options():
#     choice = hyperopt.hp.choice(
#         "removal_opt",
#         [("RandomRemoval", "WorstRemoval", "ShawRemovalPDPTW")]
#     )

#     add_to_param_dict("removal_opt", choice)
    
#     return choice


def perturb_algs():
    
    algs_data = {
        "RandomShift" : params_perturb.random_shift(),
        "ModBiasedShift" : params_perturb.mod_biased_shift(),
        "RandomExchange" : params_perturb.random_exchange()
    }
    
    
    return algs_data


# def perturb_options():
#     choice = hyperopt.hp.choice(
#         "perturb_opt",
#         [("RandomShift", "ModBiasedShift", "RandomExchange")]
#     )
    
#     add_to_param_dict("perturb_opt", choice)
    
#     return choice


def meta_algs():
    # "list_size" : (
    #     hyperopt.hp.choice(
    #         "size", 
    #         [i for i in range(100, 200)]
    #     )
    # )
    # "max_it_without_improv" : hyperopt.hp.choice(
    #     "max_it", 
    #     [i for i in range(100, 501)]
    # ),
    # "k_min" : hyperopt.hp.choice(
    #     "k_min",
    #     [i for i in range(1, 7)]
    # ),
    # "k_max" : hyperopt.hp.choice(
    #     "k_max",
    #     [i for i in range(1, 7)]
    # ),
    # "b_min" : hyperopt.hp.choice(
    #     "b_min", 
    #     [i for i in range(1,6)]
    # ),
    # "b_max" : hyperopt.hp.uniform("b_max", 0.1, 0.4),
    # "RandomRemoval" :hyperopt.hp.uniform("rr_prob", 1, 10),
    # "WorstRemoval" : hyperopt.hp.uniform("wr_prob", 1, 10),
    # "ShawRemoval" : hyperopt.hp.uniform("sr_prob", 1, 10)
    # "RandomShift" : hyperopt.hp.uniform("rs_prb", 1, 10),
    # "RandomExchange" : hyperopt.hp.uniform("re_prb", 1, 10),
    # "ModBiasedShift" : hyperopt.hp.uniform("bs_prb", 1, 10)
    # "number_of_perturb_moves" : hyperopt.hp.choice(
    #         "max_pert_math", 
    #         [i for i in range(1, 301)]
    # )
    algs_data = {
        "AGES" : params_meta.ages(),
        "LNS" : params_meta.lns(),
        "SetPartitionModel" : params_meta.set_partitioning(),
        "OriginalPerturbation" : params_meta.original_perturbation(),
        "SBMath" : params_meta.sb_math()
    }
    return algs_data


# def meta_options():
#     meta_choice = hyperopt.hp.choice(
#         "metaheuristic",
#         [
#             "AGES"
#             "LNS"
#             "SetPartitionModel"
#             "OriginalPerturbation"
#             "SBMath"
#         ]
#     )
#     return meta_choice


def solvers_algs():
    sol_algs = {
        "SolverPDPTW" : params_solver.solver_pdptw()
    }
    
    return sol_algs

# def solvers_options():
#     choice = hyperopt.hp.choice(
#         "solver_choice",
#         [
#             "SolverPDPTW"
#         ]
#     )
#     return choice

def constraints_data():
    constr_data = {
        "TimeWindowsConstraint" : params_constraints.time_windows_constraint(),
        "HomogeneousCapacityConstraint": (
            params_constraints.homogeneous_capacity_constraint()
        ),
        "PickupDeliveryConstraint": (
            params_constraints.pickup_delivery_constraint()
        ),
        "AttendAllRequests" : params_constraints.attend_all_requests()
    }
    
    return constr_data

def objectives_data():
    obj_data = {
        "ObjDistancePDPTW" : params_objectives.obj_distance_PDPTW(),
        "ObjVehiclePDPTW" : params_objectives.obj_vehicles()
    }
    
    return obj_data


def reader_data():
    reader_classes_data = {
        "ReaderJsonPDPTW" : params_files_manager.reader_json_PDPTW()
    }
    
    return reader_classes_data


def writer_data():
    writer_classes_data = {
        "WriterLiLimPDPTW" : params_files_manager.writer_li_lim_PDPTW()
    }
    
    return writer_classes_data


def route_data():
    r_data = {
        "RoutePDPTW" : params_routes.route_pdptw()
    }

    return r_data


def vertex_data():
    v_data = {
        "VertexPDPTW" : params_routes.vertex_pdptw()
    }

    return v_data


def insertion_operator_data():
    insert_data = {
        "InsertionOperatorPDPTW" : params_routes.insertion_operator_pdptw()
    }

    return insert_data


def removal_operator_data():
    remov_data = {
        "RemovalOperatorPDPTW" : params_routes.removal_operator_pdptw()
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
    
    reader_class_name = "ReaderJsonPDPTW"
    wirter_class_name = "WriterLiLimPDPTW"
    
    route_class_name = "RoutePDPTW"
    vertex_class_name = "VertexPDPTW"
    
    insertion_class_name = "InsertionOperatorPDPTW"
    removal_class_name = "RemovalOperatorPDPTW"
    
    out_data = {}
    
    out_data["objective"] = configuration["objectives"]
    out_data["constraints"] = configuration["constraints"]
    
    out_data["reader"] = {
        "ReaderJsonPDPTW" : configuration["reader"][reader_class_name]
    }
    
    out_data["writer"] = {
        "WriterLiLimPDPTW" : configuration["writer"][wirter_class_name]
    }
    
    out_data["route_class"] = {
        "RoutePDPTW" : configuration["route"][route_class_name]
    }
    
    out_data["vertex_class"] = {
        "VertexPDPTW" : configuration["vertex"][vertex_class_name]
    }
    
    out_data["insertion_operator"] = {
        "InsertionOperatorPDPTW" : (
            configuration["insertion"][insertion_class_name]
        )
    }
    
    out_data["removal_operator"] = {
        "RemovalOperatorPDPTW" : (
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


def solve_inputs(inputs, output_path, time_limit, config_file):
    global config_idx
    
    results = {}
    
    
    for i in range(len(inputs)):
        output = "".join(inputs[i].split("/")[-1].split(".")[0])
        output += "_config_" + str(config_idx) + ".txt"
        output = output_path + "all_solutions/" + output
        
        arguments = {}
        arguments["configuration_file"] = config_file
        arguments["seed"] = random.randint(0, 10000000)
        arguments["time_limit"] = time_limit
        arguments["make_log"] = True
        arguments["detail_sol"] = False
        arguments["input"] = inputs[i]
        arguments["output"] = output
        arguments["output_path"] = None
        
        
        result = solver.execute(arguments=arguments)
        results[i] = result
    
    # print(results)
    
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
    
    for result in results.values():
        if (result["solution"] is None):
            solution_costs += big_m
    
    return solution_costs


def get_obj(params):
    global config_idx
    config_idx += 1
    
    configuration, inputs, output_path, time_limit, h_opt_dict = params
    

    
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

    command_input_data = read_command_line_inputs()

    random.seed(0)
    print("STARTING SEED", 0)
    configuration = {
        "solver" : params_solver.solvers_options(),
        "solvers_algs" : solvers_algs(),

        "constructive_algs" : constructive_algs(),
        "reinsertion_algs" : reinsertion_algs(),
        "removal_algs" : removal_algs(),
        "perturb_algs" : perturb_algs(),
        "meta_algs" : meta_algs(),

        "constraints" : constraints_data(),
        "objectives" : objectives_data(),

        "writer" : writer_data(),
        "reader" : reader_data(),

        "insertion" : insertion_operator_data(),
        "removal_operator" : removal_operator_data(),

        "route" : route_data(),
        "vertex" : vertex_data(),
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
    
    
    results_conf_f = command_input_data["output_path"] + "results_configs.json"
    with open(results_conf_f, "w+") as r_conf: 
        r_conf.write(json.dumps(results_configs))

    # WRITE BEST PARAMS
    best_params_file_name = (
        command_input_data["output_path"] 
        + command_input_data["best_params_file_name"]
    )

    json_acceptable = str(best_params).replace("'", "\"")
    
    with open(best_params_file_name, "w+") as best_file:
        best_file.write(json.dumps(json.loads(json_acceptable), indent=2))

    # WRITE BEST CONFIG FILE
    best_out = (
        command_input_data["output_path"] 
        + command_input_data["best_config_file_name"]
    )
    
    best_config = hyperopt.space_eval(params, best_params)[0]
    
    with open(best_out, "w+") as best_file:
        best_file.write(json.dumps(best_config, indent=2))
        
    