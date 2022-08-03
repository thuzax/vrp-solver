import os
import sys

import json
import flask

import server_solver_util

app = flask.Flask(__name__)
host_ip = "127.0.0.1"
host_port = 6464

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
        "par-pdptw-v" : os.path.join(
            home_link, "par/pdptw-v"
        ),
        
        "dpdptw-v" : os.path.join(
            home_link, "dpdptw-v"
        ),
        "par-dpdptw-v" : os.path.join(
            home_link, "par/dpdptw-v"
        ),
        
        "dpdptw-r" : os.path.join(
            home_link, "dpdptw-r"
        ),
        "par-dpdptw-r" : os.path.join(
            home_link, "par/dpdptw-r"
        ),

        "dpdptwlf-d" : os.path.join(
            home_link, "dpdptwlf-d"
        ),
        "par-dpdptwlf-d" : os.path.join(
            home_link, "par/dpdptwlf-d"
        ),
        
        "dpdptwhf-r" : os.path.join(
            home_link, "dpdptwhf-r"
        ),
        "par-dpdptwhf-r" : os.path.join(
            home_link, "par/dpdptwhf-r"
        )
    }


@app.route("/pdptw-v", methods=["POST"])
def pdptw_v():
    func_code = "SPDPTW_V"
    data = json.loads(flask.request.json)
    solution_data = server_solver_util.solve_problem(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return json.dumps(solution_data)


@app.route("/dpdptw-v", methods=["POST"])
def dpdptw_v():
    func_code = "DPDPTW_V"
    data = json.loads(flask.request.json)
    solution_data = server_solver_util.solve_problem(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return json.dumps(solution_data)


@app.route("/dpdptw-r", methods=["POST"])
def dpdptw_r():
    func_code = "DPDPTW_R"
    data = json.loads(flask.request.json)
    solution_data = server_solver_util.solve_problem(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return json.dumps(solution_data)


@app.route("/dpdptwlf-d", methods=["POST"])
def dpdptwlf_d():
    func_code = "DPDPTWNoC_D"
    data = json.loads(flask.request.json)
    solution_data = server_solver_util.solve_problem(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return json.dumps(solution_data)


@app.route("/dpdptwhf-r", methods=["POST"])
def dpdptwhf_r():
    func_code = "DPDPTWHF_R"
    data = json.loads(flask.request.json)
    solution_data = server_solver_util.solve_problem(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    print(solution_data)
    print(json.dumps(solution_data))
    return json.dumps(solution_data)

@app.route("/par/pdptw-v", methods=["POST"])
def par_pdptw_v():
    func_code = "SPDPTW_V"
    data = json.loads(flask.request.json)
    solution_data = server_solver_util.solve_problems_parallel(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return json.dumps(solution_data)


@app.route("/par/dpdptw-v", methods=["POST"])
def par_dpdptw_v():
    func_code = "DPDPTW_V"
    data = json.loads(flask.request.json)
    solution_data = server_solver_util.solve_problems_parallel(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return json.dumps(solution_data)


@app.route("/par/dpdptw-r", methods=["POST"])
def par_dpdptw_r():
    func_code = "DPDPTW_R"
    data = json.loads(flask.request.json)
    solution_data = server_solver_util.solve_problems_parallel(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return json.dumps(solution_data)


@app.route("/par/dpdptwhf-r", methods=["POST"])
def par_dpdptwhf_r():
    func_code = "DPDPTWHF_R"
    data = json.loads(flask.request.json)
    solution_data = server_solver_util.solve_problems_parallel(func_code, data)
    if (solution_data is None):
        return "No solution found. Probably an error ocurred."
    
    return json.dumps(solution_data)


if __name__ == '__main__':
    args = sys.argv[1:]

    host_ip = "127.0.0.1"
    if (len(args) > 0):
        host_ip = args[0]

    host_port = 6464
    if (len(args) > 1):
        host_port = int(args[1])
    
    home_link = get_home_link()
    # app.run(host=host_ip, port=host_port, debug=True, threaded=True)
    app.run(host=host_ip, port=host_port, threaded=True)
