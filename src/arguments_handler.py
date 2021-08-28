import argparse
import json

from src import route_classes
from src import vertex_classes
from src import solution_classes


from src.objects_managers import ObjFunctionsObjects
from src.objects_managers import HeuristicsObjects
from src.objects_managers import ConstraintsObjects

from src.route_classes.Route import RouteSubClass
from src.vertex_classes.Vertex import VertexSubClass

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


def configure_route_class(dict_route):
    route_class_name = list(dict_route.keys())[0]
    route_class_type = getattr(
        route_classes, 
        route_class_name
    )

    RouteSubClass(route_class_type)

def configure_vertex_class(dict_vertex):
    vertex_class_name = list(dict_vertex.keys())[0]
    vertex_class_type = getattr(
        vertex_classes, 
        vertex_class_name
    )

    VertexSubClass(vertex_class_type)


def read_configuration(arguments):
    constraints_file_name = arguments["configuration_file"]

    with open(constraints_file_name, "r") as config_file:
        text = config_file.read()
        dict_data = json.loads(text)

        dict_obj_func = dict_data["objective"]
        create_obj_function_objects(dict_obj_func)

        dict_obj_func = dict_data["constraints"]
        create_constraints_objects(dict_obj_func)

        dict_obj_func = dict_data["heuristics"]
        create_heuristics_objects(dict_obj_func)

        dict_solver = dict_data["solver"]
        create_solver_object(dict_solver)

        dict_reader = dict_data["reader"]
        create_reader_object(dict_reader)

        dict_route = dict_data["route_class"]
        configure_route_class(dict_route)

        dict_vertex = dict_data["vertex_class"]
        configure_vertex_class(dict_vertex)



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

    args = parser.parse_args()

    arguments = vars(args)

    return arguments