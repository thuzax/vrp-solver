import random
import hyperopt
import pprint
import json
import math

import solver


big_m = 99999999999999999999999999999999999999


def constructive_algs():
    algs_data = {
        "BasicGreedy" : {
            "obj_func_name" : "ObjVehicles",
            "constraints_names" : [
                "AttendAllRequests",
                "PickupDeliveryConstraint",
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ]
        },
        
        "WBasicGreedy" : {
            "obj_func_name" : "ObjVehicles",
            "constraints_names" : [
                "AttendAllRequests",
                "PickupDeliveryConstraint",
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ]
        }
    }

    return algs_data


def constructive_options():
    choice = hyperopt.hp.choice(
        "constructive_opt",
        ["BasicGreedy", "WBasicGreedy"]
    )
    return choice


def reinsertion_algs():
    algs_data = {
        "KRegret" : {
            "non_insertion_cost" : 9999999999999,
            "use_modification" : False,
            "obj_func_name" : "ObjDistancePDPTW",
            "constraints_names" : [
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ]
        },
        
        "WKRegret" : {
            "non_insertion_cost" : 9999999999999,
            "obj_func_name" : "ObjDistancePDPTW",
            "constraints_names" : [
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ]
        },
        
        "RandomInsertion" : {
            "obj_func_name" : "ObjDistancePDPTW",
            "constraints_names" : [
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ]
        }
    }
    return algs_data


def reinsertion_options():
    choice = hyperopt.hp.choice(
        "reinsertion_opt",
        ["KRegret", "WKRegret"]
    )
    return choice


def removal_algs():
    algs_data = {
        "RandomRemoval" : {
            "obj_func_name" : "ObjDistancePDPTW",
            "constraints_names" : [
            ]
        },
        
        "WorstRemoval" : {
            "obj_func_name" : "ObjDistancePDPTW",
            "constraints_names" : [
            ],
            "p" : hyperopt.hp.choice("p_worst", [i for i in range(11)])
        },
        
        "ShawRemovalPDPTW" : {
            "obj_func_name" : "ObjDistancePDPTW",
            "constraints_names" : [
            ],
            "p" : hyperopt.hp.choice("p_shaw", [i for i in range(11)]),
            "phi" : hyperopt.hp.choice("phi", [i for i in range(11)]),
            "qui" : hyperopt.hp.choice("qui", [i for i in range(11)]),
            "psi" : hyperopt.hp.choice("psi", [i for i in range(11)])
        }
    }
    return algs_data


def removal_options():
    choice = hyperopt.hp.choice(
        "removal_opt",
        [("RandomRemoval", "WorstRemoval", "ShawRemovalPDPTW")]
    )
    return choice


def perturb_algs():
    algs_data = {
        "RandomShift" : {
            "obj_func_name" : "ObjVehicles",
            "constraints_names" : [
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ]
        },
        
        "ModBiasedShift" : {
            "obj_func_name" : "ObjVehicles",
            "constraints_names" : [
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ],
            "mi" : hyperopt.hp.uniform("mi_prob", 1, 10),
        },
        
        "RandomExchange" : {
            "obj_func_name" : "ObjVehicles",
            "constraints_names" : [
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ]
        }
    }
    return algs_data


def perturb_options():
    choice = hyperopt.hp.choice(
        "perturb_opt",
        [("RandomShift", "ModBiasedShift", "RandomExchange")]
    )
    return choice


def meta_algs():
     algs_data = {
        "AGES" : {
            "obj_func_name" : "ObjVehicles",
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
            "max_number_of_perturbations" : (
                hyperopt.hp.choice(
                    "max_pert", 
                    [i for i in range(1, 51)]
                )
            ),
            "number_of_perturb_moves" : (
                hyperopt.hp.choice(
                    "n_pert", 
                    [i for i in range(1, 101)]
                )
            ),
        },
        
        "LNS" : {
            "obj_func_name" : "ObjVehicles",
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
                "KRegret" : reinsertion_options(),
                "RandomRemoval" : "RandomRemoval",
                "WorstRemoval" : "WorstRemoval",
                "ShawRemoval" : "ShawRemovalPDPTW"
            },
            "stop_criteria" : "iterations",
            "max_time" : None,
            "max_time_without_improv" : None,
            "max_it" : 1001,
            "max_it_without_improv" : hyperopt.hp.choice(
                "max_it", 
                [i for i in range(100, 501)]
            ),
            "k_min" : hyperopt.hp.choice(
                "k_min",
                [i for i in range(1, 7)]
            ),
            "k_max" : hyperopt.hp.choice(
                "k_max",
                [i for i in range(1, 7)]
            ),
            "b_min" : hyperopt.hp.choice(
                "b_min", 
                [i for i in range(1,6)]
            ),
            "b_max" : hyperopt.hp.uniform("b_max", 0.1, 0.4),
            "removals_probabilities" : {
                "RandomRemoval" :hyperopt.hp.uniform("rr_prob", 1, 10),
                "WorstRemoval" : hyperopt.hp.uniform("wr_prob", 1, 10),
                "ShawRemoval" : hyperopt.hp.uniform("sr_prob", 1, 10)
            }
        },
        
        "SetPartitionModel" : {
            "obj_func_name" : "ObjVehicles",
            "constraints_names" : [
                "AttendAllRequests",
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint"
            ],
            "solver_code" : "CBC",
            "opt_time_limit" : 60
        },
        
        "OriginalPerturbation" : {
            "obj_func_name" : "ObjVehicles",
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
                "RandomShift" : hyperopt.hp.uniform("rs_prb", 1, 10),
                "RandomExchange" : hyperopt.hp.uniform("re_prb", 1, 10),
                "ModBiasedShift" : hyperopt.hp.uniform("bs_prb", 1, 10)
            }
        },

        "SBMath" : {
            "obj_func_name" : "ObjVehicles",
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
            "number_of_perturb_moves" : hyperopt.hp.choice(
                            "max_pert_math", 
                            [i for i in range(1, 301)]
                        )
        }
     }
     return algs_data


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
    return meta_choice


def solvers_algs():
    sol_algs = {
        "SolverPDPTW" : {
            "output_type" : "json",
            "obj_func_name" : "ObjVehicles",
            "construction_name" : constructive_options(),
            "metaheuristic_name" : "SBMath",
            "constraints_names" : [
                "HomogeneousCapacityConstraint",
                "TimeWindowsConstraint",
                "PickupDeliveryConstraint",
                "AttendAllRequests"
            ]
        }
    }
    return sol_algs

def solvers_options():
    choice = hyperopt.hp.choice(
        "solver_choice",
        [
            "SolverPDPTW"
        ]
    )
    return choice

def constraints_data():
    constr_data = {
        "TimeWindowsConstraint" : {
        },
        "HomogeneousCapacityConstraint": {
        },
        "PickupDeliveryConstraint": {
        },
        "AttendAllRequests" : {
        }
    }
    
    return constr_data

def objectives_data():
    obj_data = {
        "ObjDistancePDPTW" : {
        },
        "ObjVehicles" : {
        }
    }
    
    return obj_data


def reader_data():
    reader_classes_data = {
        "ReaderJsonPDPTW" : {
            "input_path" : "",
            "input_name" : "",
            "input_type" : "json"
        }
    }
    
    return reader_classes_data


def writer_data():
    writer_classes_data = {
        "WriterLiLimPDPTW" : {
            "output_path" : "./test_instances/result_files/",
            "output_type" : "txt"
        }
    }
    
    return writer_classes_data


def route_data():
    r_data = {
        "RoutePDPTW" : {
        }
    }

    return r_data


def vertex_data():
    v_data = {
        "VertexPDPTW" : {
        }
    }

    return v_data


def insertion_operator_data():
    insert_data = {
        "InsertionOperatorPDPTW" : {
        }
    }

    return insert_data


def removal_operator_data():
    remov_data = {
        "RemovalOperatorPDPTW" : {
        }
    }

    return remov_data


def make_configuration_input_file(configuration, input_config_name):
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

    print(configuration["solver"])
    solver_name = configuration["solver"]
    print(configuration["solvers_algs"])
    out_data["solver"] = {
        solver_name : configuration["solvers_algs"][solver_name]
    }
    data = json.dumps(out_data, indent=4)
    with open("teste.json", "w") as f:
        f.write(data)


def solve_inputs(inputs, config_file):
    results = []
    for i in range(len(inputs)):
        arguments = {}
        arguments["configuration_file"] = config_file
        arguments["seed"] = 10
        arguments["time_limit"] = 1
        arguments["make_log"] = True
        arguments["detail_sol"] = False
        arguments["input"] = inputs[i]
        arguments["output"] = None
        arguments["output_path"] = "./test_instances/result_files/"
        
        
        result = solver.execute(arguments=arguments)
        results.append(result)
        
    return results


def read_cost_matrix():
    pass



def calculate_solution_value(result_dict, matrix_maxis, norm_divisor):
    if (result_dict["solution"] is None):
        return big_m


def get_obj(params):
    configuration, inputs = params
    input_config_name = "./teste.json"
    
    make_configuration_input_file(configuration, input_config_name)
    
    results = solve_inputs(inputs, input_config_name)
    
    for i, result in enumerate(results):
        print(inputs[i])
        
        if (result["solution"] is None):
            print("None" + " " + "None")
            continue
        
        print(
            str(result["solution"]["solution_cost"])
            + " "
            + str(result["solution"]["solution_routes_cost"])
        )
    
    normalized_cost_divisor = 10 ** (int(math.log(len(inputs), 10)) + 1)
    
    matrices_maxis = []
    
    for inp in inputs:
        matrix = read_cost_matrix()
    
    return len(configuration)



if __name__ == "__main__":

    random.seed(0)

    configuration = {
                "solver" : solvers_options(),
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
                "vertex" : vertex_data()
                
    }

    inputs = [
        "./test_instances/input_files/new_instances/br-ms-cg-10_input.json",
        "./test_instances/input_files/new_instances/br-ms-cg-20_input.json",
        "./test_instances/input_files/new_instances/br-ms-cg-30_input.json",
        "./test_instances/input_files/new_instances/br-ms-cg-100_input.json",
        "./test_instances/input_files/new_instances/br-mg-bh-10_input.json",
        "./test_instances/input_files/new_instances/br-mg-bh-200_input.json",
        "./test_instances/input_files/SB_json/bar-n100-1.json"
    ]
    
    params = (configuration, inputs)

    best = hyperopt.fmin(
        fn=get_obj, 
        space=params, 
        algo=hyperopt.tpe.suggest, 
        max_evals=1
    )

    # pprint.pprint(best)
