from src.solution_classes.Solution import Solution
from src.objects_managers import *
from src.GenericClass import GenericClass
import time
import random
import numpy

from src import arguments_handler
from src import execution_log
from src import exceptions

from src.solvers import *
from src.instance_readers import *
from src.route_classes import *


def set_object_attributes(obj_origin, obj_destiny, attr_relation):
    for origin_attr_name, destiny_attr_name in attr_relation.items():
        origin_attr = getattr(obj_origin, origin_attr_name)
        obj_destiny.set_attribute(destiny_attr_name, origin_attr)


def set_read_objects_attributes(reader):
    solver_obj = SolverClass()

    read_sol_attr_relation = solver_obj.get_attr_relation_reader_solver()
    set_object_attributes(reader, solver_obj, read_sol_attr_relation)

    obj_funcs_objects = ObjFunctionsObjects().get_list()

    for obj_func in obj_funcs_objects:
        read_obj_f_attr_rela = obj_func.get_attr_relation_reader_func()
        set_object_attributes(reader, obj_func, read_obj_f_attr_rela)


    heuristics_objects = HeuristicsObjects().get_list()
    for heuristic in heuristics_objects:
        read_heur_attr_rela = heuristic.get_attr_relation_reader_heuristic()
        set_object_attributes(reader, heuristic, read_heur_attr_rela)
        
    constraints_objects = ConstraintsObjects().get_list()
    for constraint in constraints_objects:
        read_cons_attr_rela = constraint.get_attr_relation_solver_constr()
        set_object_attributes(reader, constraint, read_cons_attr_rela)

    reader_route_attr_relation = Route.get_reader_route_attr_relation()
    dict_attr_values = {}
    for reader_attr, route_attr in reader_route_attr_relation.items():
        reader_attr_value = getattr(reader, reader_attr)
        dict_attr_values[route_attr] = reader_attr_value
    Route.update_route_class_params(dict_attr_values)

    # solution_obj = Solution()
    # reader_solut_attr_relation = solution_obj.get_reader_solut_attr_relation()
    # set_object_attributes(reader, solution_obj, read_sol_attr_relation)



def read_input_file():
    execution_log.info_log("Reading input file...")
    reader = Reader()
    reader.read_input_file()
    set_read_objects_attributes(reader)


def solve_problem():
    solver_obj = SolverClass()
    solver_route_attr_relation = Route.get_reader_route_attr_relation()

    dict_attr_values = {}
    for solver_attr, route_attr in solver_route_attr_relation.items():
        solver_attr_value = getattr(solver_obj, solver_attr)
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

        read_input_file()
        solve_problem()


    except Exception as ex:
        exception = ex

    finally:
        if (exception is not None):
            print(exception)
            raise exception
        
        solver = SolverClass()


        execution_log.info_log("Writting Running Data...")
        end_time = time.time()
        total_time = end_time - start_time
        
        running_data = {
            "seed" : arguments["seed"],
            "time" : total_time
        }
        solver.write_final_data(running_data)
        execution_log.info_log("*Ending Program.*")
