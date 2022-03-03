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
        "pdptw-v" : os.path.join(
            home_link, "pdptw-v"
        ),
        "dpdptw-v" : os.path.join(
            home_link, "dpdptw-v"
        ),
        "dpdptw-r" : os.path.join(
            home_link, "dpdptw-r"
        ),
        "dpdptwhf-r" : os.path.join(
            home_link, "dpdptwhf-r"
        )
    }


@app.route("/pdptw-v", methods=["POST"])
def pdptw_v():
    func_code = "SPDPTW_V"
    data = json.loads(flask.request.json)
    solution_data = server_util.solve_problem(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return solution_data


@app.route("/dpdptw-v", methods=["POST"])
def dpdptw_v():
    func_code = "DPDPTW_V"
    data = json.loads(flask.request.json)
    solution_data = server_util.solve_problem(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return solution_data


@app.route("/dpdptw-r", methods=["POST"])
def dpdptw_r():
    func_code = "DPDPTW_R"
    data = json.loads(flask.request.json)
    solution_data = server_util.solve_problem(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return solution_data


@app.route("/dpdptwhf-r", methods=["POST"])
def dpdptwhf_r():
    func_code = "DPDPTWHF_R"
    data = json.loads(flask.request.json)
    solution_data = server_util.solve_problem(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return solution_data





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
