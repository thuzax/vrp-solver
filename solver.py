from src.solution_check import get_solution_check_complete_data
import time
import random
import numpy
import traceback
from func_timeout import func_timeout, FunctionTimedOut

from src.solution_methods.basic_operators.RemovalOperator import RemovalOperator
from src.solution_methods.basic_operators.InsertionOperator import InsertionOperator
from src.objects_managers import *

from src import arguments_handler, exceptions, file_log
from src import execution_log

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
    execution_log.info_log("Reading input file...")
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


def execute():
    execution_log.info_log("*Starting Program*")
    start_time = time.time()

    execution_log.info_log("Reading Input Parameters...")
    arguments = arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configuration(arguments)

    file_log.set_to_make_log(arguments["make_log"], arguments["detail_sol"])
    random.seed(arguments["seed"])
    numpy.random.seed(arguments["seed"])
    time_limit = arguments["time_limit"]


    file_log.add_info_log("Command line arguments read with no errors.")
    execution_log.info_log("Setting Random Seed")
    
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
        best_sol = solver_problem.update_and_get_best_after_timeout()
        # if (best_sol is not None):
        #     solver_problem.print_best_solution()
        #     solver_problem.print_solution_verification(best_sol, time_limit)
    
    except Exception as ex:
        exception = ex

    finally:
        end_time = time.time()
        total_time = end_time - start_time
        file_log.add_info_log(
            "Input Seed : " + str(arguments["seed"])
        )
        file_log.add_info_log(
            "Input time limit : " + str(arguments["time_limit"])
        )
        file_log.add_info_log(
            "Total execution time : " + str(total_time)
        )
        if (exception is not None):
            traceback_ex = traceback.format_exception(
                etype=type(exception), 
                value=exception, 
                tb=exception.__traceback__
            )
            file_log.add_error_log(
                "An error has ocurred\n" 
                + ''.join(traceback_ex)
            )
            
            solver_problem = SolverClass()
            file_log.write_log(
                solver_problem.output_path,
                solver_problem.output_name
            )
            raise exception
        
        solver_problem = SolverClass()
        
        execution_log.info_log("Writting Running Data and Log...")
        

        if (solver_problem.get_best_solution() is None):
            execution_log.warning_log("No solution found")
        else:
            message = "Final Solution Verification" + "\n"
            message += get_solution_check_complete_data(
                solver_problem.get_best_solution(), 
                solver_problem.constraints, 
                solver_problem.obj_func
            )
            
            message += "\n"
            file_log.add_solution_log(
                solver_problem.get_best_solution(),
                message
            )

        # print(file_log.log_data)
        file_log.write_log(
            solver_problem.output_path,
            solver_problem.output_name
        )
        execution_log.info_log("*Ending Program.*")


if __name__=="__main__":
    execute()