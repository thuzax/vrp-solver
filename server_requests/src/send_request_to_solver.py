import requests
import json
import os


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
    seed = 0
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


def send_request(problem_link_id, file_path, time=None, shutdown_link=None):

    json_input = make_json_input_dict(file_path, time)

    links = get_links()

    file_name = json_input["name"]
    time_limit = json_input["time_limit"]
    all_solutions = json_input["get_all_solutions"]

    json_input = json.dumps(json_input)

    print("Sending to", links[problem_link_id])
    print("FILE:", file_name)
    print("TIME:", time_limit)
    print("RETURN ALL?", "YES" if all_solutions else "NO")

    print(links[problem_link_id])

    r = requests.post(
        links[problem_link_id],
        json=json_input, 
        timeout=time_limit + 30
    )

    if (r.text == "No solution found. Probably an error ocurred."):
        print("ERROR ON SOLVER SERVER")
        if (shutdown_link is not None):
            requests.get(shutdown_link)
    try:
        result = json.loads(r.text)
        return result
    except Exception as ex:
        print("Could not load solution json")
        raise ex
        
