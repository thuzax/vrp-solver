import json

from config_best_dicts import objectives_dicts
from config_best_dicts import constraints_dicts
from config_best_dicts import reader_dicts
from config_best_dicts import writer_dicts
from config_best_dicts import routes_classes_dicts
from config_best_dicts import vertex_classes_dicts
from config_best_dicts import insertion_classes_dicts
from config_best_dicts import removal_classes_dicts
from config_best_dicts import constructive_dicts
from config_best_dicts import insertions_dicts
from config_best_dicts import removals_dicts
from config_best_dicts import perturb_dicts
from config_best_dicts import meta_dicts
from config_best_dicts import solver_dicts




def get_configuration_dict(best_params, problem):
    out_data = {}
    out_data["objective"] = objectives_dicts.objectives_data(
        best_params, 
        problem
    )
    out_data["constraints"] = constraints_dicts.constraints_data(
        best_params, 
        problem
    )
    
    reader_data = reader_dicts.reader_data(best_params, problem)
    reader_class_name = list(reader_data.keys())[0]

    out_data["reader"] = {
        reader_class_name : reader_data[reader_class_name]
    }
    
    writer_data = writer_dicts.writer_data(best_params, problem)
    writer_class_name = list(writer_data.keys())[0]
    out_data["writer"] = {
        writer_class_name : writer_data[writer_class_name]
    }
    
    r_data = routes_classes_dicts.route_data(best_params, problem)
    route_class_name = list(r_data.keys())[0]
    out_data["route_class"] = {
        route_class_name : r_data[route_class_name]
    }
    
    v_data = vertex_classes_dicts.vertex_data(best_params, problem)
    vertex_class_name = list(v_data.keys())[0]
    out_data["vertex_class"] = {
        vertex_class_name : v_data[vertex_class_name]
    }
    
    insertion_data = insertion_classes_dicts.insertion_operator_data(
        best_params, 
        problem
    )
    insertion_class_name = list(insertion_data.keys())[0]
    out_data["insertion_operator"] = {
        insertion_class_name : (
            insertion_data[insertion_class_name]
        )
    }
    
    removal_data = removal_classes_dicts.removal_operator_data(
        best_params, 
        problem
    )
    removal_class_name = list(removal_data.keys())[0]
    out_data["removal_operator"] = {
        removal_class_name : (
            removal_data[removal_class_name]
        )
    }
    
    out_data["solution_methods"] = {}

    algs_keys = [
        "constructive_algs",
        "reinsertion_algs",
        "removal_algs",
        "perturb_algs",
        "meta_algs"
    ]

    constructive_algs = constructive_dicts.constructive_data(
        best_params, 
        problem
    )
    
    for name, value in constructive_algs.items():
        out_data["solution_methods"][name] = value

    reinsertion_algs = insertions_dicts.reinsertion_data(best_params, problem)
    for name, value in reinsertion_algs.items():
        out_data["solution_methods"][name] = value

    
    removal_algs = removals_dicts.removal_data(best_params, problem)
    for name, value in removal_algs.items():
        out_data["solution_methods"][name] = value


    perturb_algs = perturb_dicts.perturb_data(best_params, problem)
    for name, value in perturb_algs.items():
        out_data["solution_methods"][name] = value


    meta_algs = meta_dicts.meta_algs_data(best_params, problem)
    for name, value in meta_algs.items():
        out_data["solution_methods"][name] = value

    solver_data = solver_dicts.solvers_data(best_params, problem)
    solver_name = list(solver_data.keys())[0]

    out_data["solver"] = {
        solver_name : solver_data[solver_name]
    }
    return out_data
    