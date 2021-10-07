import argparse
import json
from src.vertex_classes import Vertex

from src import route_classes
from src import vertex_classes
from src import solution_classes
from src.solution_methods import basic_operators


from src.objects_managers import ObjFunctionsObjects
from src.objects_managers import HeuristicsObjects
from src.objects_managers import ConstraintsObjects

from src.route_classes.Route import Route


from src.objects_creation_manager import create_class_by_name

def create_obj_function_objects(dict_obj_func):
    obj_func_classes_names = list(dict_obj_func.keys())

    for obj_func_name in obj_func_classes_names:
        obj_func_object = create_class_by_name(
            obj_func_name,
            dict_obj_func[obj_func_name]
        )


def create_constraints_objects(dict_constraints):
    constraints_classes_names = list(dict_constraints.keys())

    for constraints_name in constraints_classes_names:
        constraints_object = create_class_by_name(
            constraints_name,
            dict_constraints[constraints_name]
        )


def create_heuristics_objects(dict_heuristics):
    heuristics_classes_names = list(dict_heuristics.keys())

    for heuristics_name in heuristics_classes_names:
        heuristics_object = create_class_by_name(
            heuristics_name,
            dict_heuristics[heuristics_name]
        )
    
    for heuristic in HeuristicsObjects().get_list():
        obj_func = ObjFunctionsObjects().get_by_name(heuristic.obj_func_name)
        heuristic.set_attribute("obj_func", obj_func)

        constraints = []
        for constraint_name in heuristic.constraints_names:
            constraint = ConstraintsObjects().get_by_name(constraint_name)
            constraints.append(constraint)
        
        heuristic.set_attribute("constraints", constraints)

        if (hasattr(heuristic, "acceptance_algorithm")):
            alg_data = heuristic.acceptance_algorithm_data
            obj = create_accept_criteria_object(alg_data)
            heuristic.acceptance_algorithm = obj

        if (hasattr(heuristic, "local_operators_names")):
            dict_operators = {}
            for op, op_name in heuristic.local_operators_names.items():
                dict_operators[op] = HeuristicsObjects().get_by_name(op_name)

            heuristic.define_local_searches_operators(dict_operators)


def create_accept_criteria_object(dict_accept_crit):
    accept_crit_name = list(dict_accept_crit.keys())[0]
    accept_crit_object = create_class_by_name(
        accept_crit_name,
        dict_accept_crit[accept_crit_name]
    )
    return accept_crit_object
    


def create_solver_object(dict_solver):
    solver_class_name = list(dict_solver.keys())[0]
    
    solver_obj = create_class_by_name(
        solver_class_name, 
        dict_solver[solver_class_name]
    )

    obj_func = ObjFunctionsObjects().get_by_name(solver_obj.obj_func_name)
    solver_obj.set_attribute("obj_func", obj_func)

    solver_obj.update_heuristics_data()

    constraints = []
    for constraint_name in solver_obj.constraints_names:
        constraint = ConstraintsObjects().get_by_name(constraint_name)
        constraints.append(constraint)
    
    solver_obj.set_attribute("constraints", constraints)


def create_reader_object(dict_reader):
    reader_class_name = list(dict_reader.keys())[0]

    reader_obj = create_class_by_name(
        reader_class_name, 
        dict_reader[reader_class_name]
    )


def create_writer_object(dict_writer):
    writer_class_name = list(dict_writer.keys())[0]

    writer_obj = create_class_by_name(
        writer_class_name, 
        dict_writer[writer_class_name]
    )

def configure_route_class(dict_route):
    route_class_name = list(dict_route.keys())[0]
    route_class_type = getattr(
        route_classes, 
        route_class_name
    )

    Route.set_class(route_class_type)


def configure_vertex_class(dict_vertex):
    vertex_class_name = list(dict_vertex.keys())[0]
    vertex_class_type = getattr(
        vertex_classes, 
        vertex_class_name
    )

    Vertex.set_class(vertex_class_type)


def create_operator_class(dict_insertion_op):
    insertion_op_class_name = list(dict_insertion_op.keys())[0]
    create_class_by_name(
        insertion_op_class_name,
        dict_insertion_op[insertion_op_class_name]
    )


def read_configuration(arguments):
    constraints_file_name = arguments["configuration_file"]

    with open(constraints_file_name, "r") as config_file:
        text = config_file.read()
        dict_data = json.loads(text)

        dict_obj_func = dict_data["objective"]
        create_obj_function_objects(dict_obj_func)

        dict_obj_func = dict_data["constraints"]
        create_constraints_objects(dict_obj_func)

        dict_obj_func = dict_data["solution_methods"]
        create_heuristics_objects(dict_obj_func)

        dict_solver = dict_data["solver"]
        create_solver_object(dict_solver)

        dict_reader = dict_data["reader"]
        create_reader_object(dict_reader)
        
        dict_writer = dict_data["writer"]
        create_writer_object(dict_writer)

        dict_route = dict_data["route_class"]
        configure_route_class(dict_route)

        dict_vertex = dict_data["vertex_class"]
        configure_vertex_class(dict_vertex)

        dict_insertion_op = dict_data["insertion_operator"]
        create_operator_class(dict_insertion_op)

        dict_removal_op = dict_data["removal_operator"]
        create_operator_class(dict_removal_op)



def parse_command_line_arguments():
    """Manage the command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--set-config-file",
        dest="configuration_file",
        help="parameter configuration json file to be used. The file will have priority over the command line arguments if there conflicts in parameters",
        action="store",
        default=None,
        required=True
    )

    parser.add_argument(
        "--set-seed",
        dest="seed",
        help="set the random function seed.",
        action="store",
        default=None,
        type=int,
        required=False
    )

    parser.add_argument(
        "--set-time-limit",
        dest="time_limit",
        help="set the time limit for a timeout.",
        action="store",
        default=None,
        type=int,
        required=False
    )

    parser.add_argument(
        "--make-log",
        dest="make_log",
        help="if this flag is set, a log file will be created",
        action="store_true",
        default=False,
        required=False
    )

    parser.add_argument(
        "--detail-solution-log",
        dest="detail_sol",
        help="if this flag is set and --make-log is set, the log file will add the order of clientes in the routes whenever a solution is inserted in log",
        action="store_true",
        default=False,
        required=False
    )

    args = parser.parse_args()

    arguments = vars(args)

    return arguments