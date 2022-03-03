import os
from random import seed
import sys

import json
import flask

import server_util

app = flask.Flask(__name__)
host_ip = "127.0.0.1"
host_port = 5151

def get_home_link():
    return "http://" + host_ip + ":" + str(host_port)

@app.route('/')
def index():
    home_link = get_home_link()
    print(home_link)
    return {
        "st_min_vehicles" : os.path.join(
            home_link, "vrp-static-min-vehicles-opt"
        ),
        "dy_min_vehicles" : os.path.join(
            home_link, "vrp-dynamic-min-vehicles-opt"
        )
        
    }


@app.route("/vrp-static-min-vehicles-opt", methods=["POST"])
def static_min_vehicles():
    print("------------------------------------------------")
    func_code = "SPDPTW_V"
    data = json.loads(flask.request.json)
    input_path = server_util.create_input_file(func_code, data)    
    config_file = server_util.get_config_file(func_code)
    
    time_limit = None
    if ("time_limit" in data.keys()):
        time_limit = data["time_limit"]

    seed = None
    if ("seed" in data.keys()):
        seed = data["seed"]


    data = server_util.run_solver(input_path, config_file, time_limit, seed)
    print("------------------------------------------------")

    return "Solve static"


@app.route("/vrp-dynamic-min-vehicles-opt", methods=["POST"])
def dynamic_min_vehicles():
    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    func_code = "DPDPTW_V"
    data = json.loads(flask.request.json)

    server_util.create_input_file(func_code, data)
    config_file = server_util.get_config_file(func_code)

    print("++++++++++++++++++++++++++++++++++++++++++++++++")

    return "Solve dynamic"

if __name__ == '__main__':
    args = sys.argv[1:]

    host_ip = "127.0.0.1"
    if (len(args) > 0):
        host_ip = args[0]

    host_port = 5151
    if (len(args) > 1):
        host_port = int(args[1])
    
    home_link = get_home_link()
    app.run(host=host_ip, port=host_port, debug=True, threaded=True)
