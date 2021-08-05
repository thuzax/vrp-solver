import time
import random
import numpy

from src import arguments_handler
from src import execution_log
from src import exceptions

from src.solvers import *
from src.instance_readers import *
from src.route_classes import *

def read_input_file():
    execution_log.info_log("Reading input file...")
    reader = Reader()
    
    reader.read_input_file()

    read_sol_attr_relation = reader.get_reader_solver_attributes_relation()
    for reader_attr_name, solver_attr_name in read_sol_attr_relation.items():
        reader_attr = getattr(reader, reader_attr_name)
        solver.set_attribute(solver_attr_name, reader_attr)


def solve_problem():
    solver_obj = SolverClass()
    
    solver_route_attr_relation = Route.get_solver_route_attribute_relation()


    dict_attr_values = {}
    for solver_attr, route_attr in solver_route_attr_relation.items():
        solver_attr_value = getattr(solver, solver_attr)
        dict_attr_values[route_attr] = solver_attr_value
    
    Route.update_route_class_params(dict_attr_values)

    solver_obj.solve()

if __name__=="__main__":
    execution_log.info_log("*Starting Program*")
    start_time = time.time()

    execution_log.info_log("Reading Input Parameters...")
    arguments = arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configuration(arguments)

    execution_log.info_log("Setting Random Seed")
    random.seed(arguments["seed"])
    numpy.random.seed(arguments["seed"])

    exception = None
    try:

        solver = SolverClass()
        read_input_file()
        solve_problem()

        # print(solver.__dict__)

    except Exception as ex:
        exception = ex

    finally:
        if (exception is not None):
            print(exception)
            raise exception
        
        execution_log.info_log("Writting Running Data...")
        end_time = time.time()
        total_time = end_time - start_time
        
        running_data = {
            "seed" : arguments["seed"],
            "time" : total_time
        }

        solver.write_final_data(running_data)
        execution_log.info_log("*Ending Program.*")
