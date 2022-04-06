import multiprocessing
import random
import sys
import threading
import flask
import json

import server_arguments_handler
from src.RequestsStorage import RequestsStorage
from src import InstanceData
from src import server_requests_util

app = flask.Flask(__name__)
args = None

time_slices = None
current_time_slice_id = None

def get_home_link():
    return "http://" + args["host_ip"] + ":" + str(args["host_port"])

@app.route('/')
def index():
    home_link = get_home_link()
    print(home_link)
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
    
    print(result)
    print(len(RequestsStorage().get_all_requests()))
    return result


if __name__ == '__main__':
    args = server_arguments_handler.parse_command_line_arguments()

    if (args["is_test"]):
        server_requests_util.initialize_instance(
            args["test_instance_path"]
        )
        args["horizon"] = InstanceData().horizon * 60

    print(args)

    time_slices = server_requests_util.create_time_slices(
        args["time_slice_size"], 
        args["horizon"]
    )

    current_time_slice_id = 0

    # print("TIME SLICES:")
    # print(time_slices)
    print("TIME SLICES SIZE:")
    print(len(time_slices))
    
    sema = threading.Semaphore(1)
    t = threading.Thread(
        target=server_requests_util.solve_time_slices_problems,
        args=(
            time_slices, 
            current_time_slice_id,
        )
    )
    t.start()

    home_link = get_home_link()
    app.run(
        host=args["host_ip"], 
        port=args["host_port"], 
        debug=True, 
        threaded=True
    )

    t.join()

