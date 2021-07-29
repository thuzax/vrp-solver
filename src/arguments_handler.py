import argparse
import json

from src import solvers

def create_solver_objects(dict_solver):
    solver_class_name = list(dict_solver.keys())[0]
    
    solver_class_type = getattr(
        solvers, 
        solver_class_name
    )

    solver_class = solver_class_type()
    for attribute, value in dict_solver[solver_class_name].items():
        solver_class.set_attribute(attribute, value)



def read_configuration(arguments):
    constraints_file_name = arguments["configuration_file"]

    with open(constraints_file_name, "r") as config_file:
        text = config_file.read()
        dict_data = json.loads(text)

        dict_solver = dict_data["solver"]
        create_solver_objects(dict_solver)


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