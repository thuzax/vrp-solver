import requests
import json
import os
import random
import sys
import time

import verify_solution

def get_links():
    r = requests.get("http://127.0.0.1:6464")
    links = json.loads(r.text)
    
    # print(links)

    return links

def make_json_input_dict(file_path, time_limit=None):
    with open(file_path, "r") as input_file:
        input_data = json.loads(input_file.read())
    
    file_name = os.path.basename(file_path)

    # exit(0)
    # time limit for the solver
    if (time_limit is None):
        time_limit = 30
    # seed for the solver
    seed = random.randint(0, 10000000)
    # seed = 0
    # if True returns all solutions found with the solver
    all_solutions = False


    json_input = {
        "name" : file_name,
        "file" : input_data,
        "time_limit" : time_limit,
        "seed" : seed,
        "get_all_solutions" : all_solutions
    }

    return json_input


def send_request(
    problem_link_id, 
    file_path, 
    time=None, 
    shutdown_link=None,
    output_path=None    
):

    json_input = make_json_input_dict(file_path, time)
    if (output_path is not None):
        json_input["output_path"] = output_path

    links = get_links()

    file_name = json_input["name"]
    time_limit = json_input["time_limit"]
    all_solutions = json_input["get_all_solutions"]
    seed = json_input["seed"]

    json_input = json.dumps(json_input)

    print("Sending to", links[problem_link_id])
    print("FILE:", file_name)
    print("TIME:", time_limit)
    print("SEED:", seed)
    print("RETURN ALL?", "YES" if all_solutions else "NO")

    # print(links[problem_link_id])

    r = requests.post(
        links[problem_link_id],
        json=json_input, 
        timeout=time_limit + 60
    )

    if (r.text == "No solution found. Probably an error ocurred."):
        # print("ERROR ON SOLVER SERVER")
        if (shutdown_link is not None):
            requests.get(shutdown_link)
        raise(Exception(r.text))
    try:
        result = json.loads(r.text)
        return result
    except Exception as ex:
        # print("Could not load solution json")
        raise ex
        

def verify_static_solution(
    input_file, 
    input_complete_path,
    output_run_dir, 
    problem
):
    inputs = os.path.join(output_run_dir, "inputs")

    ver_dir = os.path.split(os.path.split(output_run_dir)[0])[0]


    ver_file_name = os.path.join(ver_dir, "verification.txt")
    with open(ver_file_name, "w") as v:
        pass

    output_path = os.path.join(
        output_run_dir,
        (
            input_file.split(".")[0] 
            + "_sol_log.json"
        )
    )

    text = verify_solution.verify(
        (input_complete_path, output_path, problem, "-a")
    )

    with open(ver_file_name, "a") as file_ver:
        file_ver.write(text)


if __name__ == "__main__":
    args = sys.argv[1:]

    if (len(args) < 2):
        print("Needs input and output dirs with test instances and problem")
        exit(0)

    host_data = {
        "ip" : "127.0.0.1",
        "port" : "6464"
    }

    tests_dir = args[0]
    output_dir = args[1]
    problem = args[2]

    if (not os.path.exists(output_dir)):
        os.makedirs(output_dir)
        

    files_names = os.listdir(tests_dir)
    files_names = [item for item in files_names if item[-5:] == ".json"]

    # print(tests_dir)
    print(files_names)
    # files_names = [files_names[2]]
    # files_names = files_names[:1]

    n_runs = 5

    time_limit = 600

    for i in range(n_runs):
        for file_name in files_names:
            print("=" * 80)

            run_name = file_name.split(".")[0] + "_run_" + str(i+1)
            output_run_dir = os.path.join(
                "..",
                output_dir,
                run_name
            )

            if (not os.path.exists(output_run_dir)):
                os.makedirs(output_run_dir)
            
            input_file = os.path.join(tests_dir, file_name)
            
            start_time = time.time()

            print(input_file)

            result = send_request(
                "dpdptwlf-d", 
                file_path=input_file, 
                time=time_limit, 
                output_path=output_run_dir
            )

            verify_static_solution(
                file_name, 
                os.path.join(tests_dir, file_name),
                os.path.join(
                    output_dir, 
                    run_name, 
                    "outputs", 
                    file_name.split(".")[0]
                ), 
                problem
            )
            print("EXEC TIME: " + str(time.time() - start_time))

            print("=" * 80)


