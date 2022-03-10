from src import solvers
from src.GenericClass import GenericClass
from src.solution_check import get_solution_check_complete_data
import time
import random
import numpy
import traceback
from func_timeout import func_timeout, FunctionTimedOut
from src.solution_methods.SolutionMethod import SolutionMethod

from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
from src.objects_managers import *

from src import arguments_handler, exceptions, file_log
from src import execution_log
from src.solution_writers import Writer
from src.solution_writers.WriterLiLimPDPTW import WriterLiLimPDPTW

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

    i_op = InsertionOperator()
    read_insert_op_rela = i_op.get_attr_relation_reader_insert_op()
    set_object_attributes(reader, i_op, read_insert_op_rela)

    r_op = RemovalOperator()
    read_remov_op_rela = r_op.get_attr_relation_reader_remov_op()
    set_object_attributes(reader, r_op, read_remov_op_rela)


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
    execution_log.info_log("Reading input file: " + Reader().get_file_name())
    reader = Reader()
    reader.read_input_file()
    set_read_objects_attributes(reader)
    
    file_log.add_info_log("Input file read with no errors.")
    execution_log.info_log("File reading finished.")


def solve_problem():
    execution_log.info_log("Starting to solve...")

    solver_obj = SolverClass()
    solver_obj.solve()
    
    execution_log.info_log("Finished.")


def run():
    read_input_file()
    solve_problem()


def initialize(arguments):
    execution_log.info_log("*Starting Program*")

    arguments_handler.read_configuration(arguments)

    file_log.set_to_make_log(
        make_log_argument=arguments["make_log"], 
        out_path=Writer().output_path,
        out_name=Writer().output_name,
        detail_solution=arguments["detail_sol"]
    )
    
    file_log.add_info_log(
        "Input Seed : " + str(arguments["seed"])
    )
    file_log.add_info_log(
            "Input time limit : " + str(arguments["time_limit"])
        )
    
    file_log.add_info_log("Command line arguments read with no errors.")
    execution_log.info_log("Setting Random Seed")
    
    random.seed(arguments["seed"])
    numpy.random.seed(arguments["seed"])


def write_error(exception):
    traceback_ex = traceback.format_exception(
        etype=type(exception), 
        value=exception, 
        tb=exception.__traceback__
    )
    file_log.add_error_log(
        "An error has ocurred\n" 
        + ''.join(traceback_ex)
    )
    
    # Writer().write_log()


def write_solution():
    solver_problem = SolverClass()
    Writer().write_solution(solver_problem.get_best_solution())
            
    log_message = "Final Solution Verification" + "\n"
    log_message += get_solution_check_complete_data(
        solver_problem.get_best_solution(), 
        solver_problem.constraints, 
        solver_problem.obj_func
    )
    
    log_message += "\n"
    log_message += "Best Solution: \n"
    file_log.add_solution_log(
        solver_problem.get_best_solution(),
        log_message
    )


def make_solution_dict(total_time, arguments):
    solver_problem = SolverClass()
    
    solution_dict = {}
    solution_dict["solution"] = solver_problem.get_best_solution_dict()
    solution_dict["time"] = total_time
    solution_dict["seed"] = arguments["seed"]
    solution_dict["input"] = Reader().get_file_name()
    solution_dict["config_file"] = arguments["configuration_file"]
    solution_dict["output"] = Writer().get_output_file_name()
    solution_dict["log_file"] = file_log.get_log_file_name()
    
    return solution_dict


def clear():
    for child_class in GenericClass.__subclasses__():
        child_class.clear()


def execute(arguments):
    start_time = time.time()
    
    initialize(arguments)
    time_limit = arguments["time_limit"]

    exception = None

    try:

        if (time_limit is not None):
            func_timeout(time_limit, run)
        else:
            run()

    except FunctionTimedOut:
        solver_problem = SolverClass()
        file_log.add_warning_log("Time Limit Exceeded")
        execution_log.warning_log("Time Limit Exceeded")
        solver_problem.update_and_get_best_after_timeout()
        
    
    except Exception as ex:
        exception = ex

    finally:
        end_time = time.time()
        total_time = end_time - start_time
        file_log.add_info_log(
            "Algorithm execution time : " + str(total_time)
        )
        

        if (exception is not None):
            write_error(exception)
            raise exception


        execution_log.info_log(
            "Writting Solution and Log (if there is): "
            + str(Writer().get_output_file_name())
        )
        solver_problem = SolverClass()
        if (solver_problem.get_best_solution() is None):
            execution_log.warning_log("No solution found")
        
        else:
            write_solution()


        solution_data_dict = make_solution_dict(total_time, arguments)
        
        file_log.write_solution_data_dict_in_json(solution_data_dict)

        # Writer().write_log()
        execution_log.info_log("*Ending Program.*")
        clear()
        return solution_data_dict


if __name__=="__main__":
    execution_log.info_log("Reading Input Parameters...")
    arguments = arguments_handler.parse_command_line_arguments()
    print(execute(arguments))