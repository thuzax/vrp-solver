import multiprocessing
import random
import sys
import threading
import flask
import json
import os
import signal

import server_arguments_handler
from src.CurrentSolution import CurrentSolution
from src.RequestsStorage import RequestsStorage
from src import InstanceData
from src import server_requests_util

app = flask.Flask(__name__)
arguments = None

time_slices = None
current_time_slice_id = None

def get_home_link():
    return "http://" + arguments["host_ip"] + ":" + str(arguments["host_port"])


def get_shutdown_link():
    return (
        "http://" + arguments["host_ip"] + ":" + str(arguments["host_port"])
        + "/shutdown"
    )

@app.route('/')
def index():
    home_link = get_home_link()
    return {
        "SERVER ON"
    }


@app.route('/make_request', methods=["POST"])
def add_request():
    global current_time_slice_id

    data = json.loads(flask.request.json)
    
    result = server_requests_util.add_request(
        data, 
        time_slices, 
        current_time_slice_id
    )
    
    # probability = random.randint(1,100)

    # change_time_slice = (
    #     True if (
    #          probability > 80 
    #         and current_time_slice_id < (len(time_slices) - 1)
    #     ) 
    #     else False
    # )
    
    # if (change_time_slice):
    #     current_time_slice_id += 1
    
    # print(result)
    # print(len(RequestsStorage().get_all_requests()))
    return result


@app.get('/shutdown')
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return "OK"


def run(run_server):
    time_slices = server_requests_util.create_time_slices(
        arguments["time_slice_size"], 
        arguments["horizon"]
    )

    time_limit = arguments["time_limit"]

    current_time_slice_id = 0

    output_path = arguments["output_path"]
    
    print("TIME SLICES SIZE:")
    print(len(time_slices))

    server_requests_util.write_on_log(
        "NUMBER TIME SLICES: " 
        + str(len(time_slices))
    )


    if (run_server):
        sema = threading.Semaphore(1)
        shutdown_link = get_shutdown_link()
        t1 = threading.Thread(
            target=server_requests_util.solve_time_slices_problems,
            args=(
                time_slices, 
                current_time_slice_id,
                time_limit,
                arguments["problem"],
                log_dir_name,
                shutdown_link,
                output_path
            )
        )
        t1.setDaemon(True)
        t1.start()
        
        home_link = get_home_link()
        app.run(
            host=arguments["host_ip"], 
            port=arguments["host_port"], 
            debug=True, 
            threaded=True
        )
        try:
            t1.join()
        except KeyboardInterrupt as kbi:
            t1.join()
    else:
        server_requests_util.solve_from_instance(
            time_slices, 
            time_limit,
            arguments["problem"],
            log_dir_name,
            output_path
        )


if __name__ == '__main__':
    arguments = server_arguments_handler.parse_command_line_arguments()

    run_server = True
    if (arguments["is_test"]):
        server_requests_util.initialize_instance(
            arguments["test_instance_path"],
            arguments["problem"]
        )

        log_dir_name = (
            os.path.basename(arguments["test_instance_path"]).split(".")[-2]
        )

        if ("output_path" in arguments):
            server_requests_util.create_directory_log_path(
                log_dir_name, 
                arguments["output_path"]
            )
        else:
            server_requests_util.create_directory_log_path(log_dir_name)


        if (arguments["horizon"] is None):
            arguments["horizon"] = InstanceData().horizon

        if (arguments["test_directly_from_instance"]):
            run_server = False

    if (arguments["horizon"] is None):
        arguments["horizon"] = 600

    # print(arguments)

    

    # print("TIME SLICES:")
    # print(time_slices)

    
    try:
        run(run_server)
    except Exception as ex:
        server_requests_util.write_on_log(str(ex))
        raise ex
    
    


    print("ENDING")

