import requests
import json

def simple_test(file_path):
    r = requests.get("http://127.0.0.1:6464")
    links = json.loads(r.text)
    print(links)

    with open(file_path, "r") as input_file:
        input_data = json.loads(input_file.read())
    
    file_name = file_path.split("/")[-1]

    json_input = json.dumps({
        "name" : file_name,
        "file" : input_data,
        "time_limit" : 30,
        "seed" : 0
    })

    r_static = requests.post(links["st_min_vehicles"], json=json_input)
    print(r_static.text)

    r_dynamic = requests.post(links["dy_min_vehicles"], json=json_input)
    print(r_dynamic.text)

simple_test("br-mg-bh-10_input.json")
simple_test("../test_instances/input_files/new_instances/br-mg-bh-200_input.json")