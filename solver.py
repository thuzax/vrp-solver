import time

from src import arguments_handler
from src import execution_log
from src import exceptions

from src.solvers import *


if __name__=="__main__":
    execution_log.info_log("*Starting Program*")
    start_time = time.time()

    execution_log.info_log("Reading Input Parameters...")
    arguments = arguments_handler.parse_command_line_arguments()
    arguments_handler.read_configuration(arguments)

    solver = SartoriBuriolPDPTW()


    print(solver.__dict__)

    exception = None
    try:
        pass

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
