import requests
import json

def get_links():
    r = requests.get("http://127.0.0.1:6464")
    links = json.loads(r.text)
    
    # print(links)

    return links

def make_json_input_dict(file_path):
    with open(file_path, "r") as input_file:
        input_data = json.loads(input_file.read())
    
    file_name = file_path.split("/")[-1]

    # time limit for the solver
    time_limit = 120
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


def simple_test(problem_link_id, file_path):

    json_input = make_json_input_dict(file_path)

    links = get_links()

    file_name = json_input["name"]
    time_limit = json_input["time_limit"]
    all_solutions = json_input["get_all_solutions"]

    json_input = json.dumps(json_input)

    print("Sending to", links[problem_link_id])
    print("FILE:", file_name)
    print("TIME:", time_limit)
    print("RETURN ALL?", "YES" if all_solutions else "NO")

    r = requests.post(
        links[problem_link_id],
        json=json_input, 
        timeout=time_limit + 30
    )
    print("Returned")
    print(r.text)
    print()
    print()
    print()
    


def simple_parallel_test(problem_link_id, file_path, number_of_rep):
    sum_time_limit = 0
    all_json_input = []
    for i in range(number_of_rep):
        json_input = make_json_input_dict(file_path)
        links = get_links()
        
        prefix = json_input["name"].split(".")[0]
        suffix = json_input["name"].split(".")[1]
        json_input["name"] =  prefix + "_" + str(i) + "." + suffix
        
        time_limit = json_input["time_limit"]
        sum_time_limit += time_limit
        
        json_input["seed"] = i

        all_json_input.append(json_input)

    print("Sending to", links[problem_link_id])
    print("NUMBER OF ITEMS:", number_of_rep)
    print("SUM TIME:", sum_time_limit)
    print("TIME:", sum_time_limit/number_of_rep)
    print("INPUTS:")
    for item in all_json_input:
        print(item["name"])
    print()

    all_json_input = json.dumps(all_json_input)
    r = requests.post(
        links[problem_link_id],
        json=all_json_input, 
        timeout=sum_time_limit + 30
    )
    print("Returned")
    print(r.text)
    print()
    print()
    print()
    


# # PDPTW MIN VEHICLE
# simple_test("pdptw-v", "../test_instances/input_files/SB_json/bar-n100-2.json")

# # DPDPTW MIN VEHICLE
# simple_test("dpdptw-v", "../test_instances/input_files/SB_json/bar-n100-1_fixed.json")
simple_test("dpdptw-v", "../test.json")

# # DPDPTW MAX REQUESTS/LIMITED FLEET
# simple_test("dpdptw-r", "../test_instances/input_files/SB_json/bar-n100-1_fixed_limited_fleet.json")

# # DPDPTW MAX REQUESTS / LIMITED HYBRID FLEET
# simple_test("dpdptwhf-r", "../test_instances/input_files/SB_json/bar-n100-1_fixed_limited_heter_fleet.json")

# # PARALLEL PDPTW MIN VEHICLE
# simple_parallel_test(
#     "par-pdptw-v", 
#     "../test_instances/input_files/SB_json/bar-n100-1.json",
#     4
# )

# # PARALLEL DPDPTW MIN VEHICLE
# simple_parallel_test(
#     "par-dpdptw-v", 
#     "../test_instances/input_files/SB_json/bar-n100-1_fixed.json",
#     4
# )

# # PARALLEL DPDPTW MAX REQUESTS/LIMITED FLEET
# simple_parallel_test(
#     "par-dpdptw-r", 
#     "../test_instances/input_files/SB_json/bar-n100-1_fixed_limited_fleet.json",
#     4
# )

# # PARALLEL DPDPTW MAX REQUESTS / LIMITED HYBRID FLEET
# simple_parallel_test(
#     "par-dpdptwhf-r", 
#     "../test_instances/input_files/SB_json/bar-n100-1_fixed_limited_heter_fleet.json",
#     4
# )