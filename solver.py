import time

from src import arguments_handler
from src.solver import *


if __name__=="__main__":
    arguments = arguments_handler.parse_command_line_arguments()
    start_time = time.time()

    solver = SartoriBuriolPDPTW()

    solver.output_path = "./"
    solver.output_name = "teste"

    exception = None
    try:
        pass

    except Exception as ex:
        exception = ex

    finally:
        if (exception is not None):
            print(exception)
            raise exception
        
        end_time = time.time()
        total_time = end_time - start_time
        
        running_data = {
            "seed" : arguments["seed"],
            "time" : total_time
        }

        solver.write_final_data(running_data)