import requests
import json

def simple_test(file_path):
    r = requests.get("http://127.0.0.1:6464")
    links = json.loads(r.text)
    print(links)

    with open(file_path, "r") as input_file:
        input_data = json.loads(input_file.read())
    
    file_name = file_path.split("/")[-1]

    tl = 5
    seed = 0

    json_input = json.dumps({
        "name" : file_name,
        "file" : input_data,
        "time_limit" : tl,
        "seed" : seed
    })

    r_static = requests.post(
        links["pdptw-v"],
        json=json_input, 
        timeout=tl + 30
    )
    print(r_static.text)


    r_dynamic_v = requests.post(
        links["dpdptw-v"],
        json=json_input, 
        timeout=tl + 30
    )
    print(r_dynamic_v.text)

    r_dynamic_r = requests.post(
        links["dpdptw-r"],
        json=json_input, 
        timeout=tl + 30
    )
    print(r_dynamic_r.text)

    r_dynamic_hf_r = requests.post(
        links["dpdptwhf-r"],
        json=json_input, 
        timeout=tl + 30
    )
    print(r_dynamic_hf_r.text)

simple_test("../test_instances/input_files/new_instances/br-mg-bh-200_input.json")