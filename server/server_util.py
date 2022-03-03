import json
import os
import sys
import subprocess

def get_input_file_path(func_code, file_name):
    file_complete_path = os.path.join(
        ".", "inputs", str(func_code) + "_" + str(file_name)
    )
    return file_complete_path


def write_input_file(path, data):
    with open(path, "w") as input:
        input.write(json.dumps(data))


def create_input_file(func_code, data):
    input_name = data["name"]
    input_data = data["file"]

    file_complete_path = get_input_file_path(func_code, input_name)
    write_input_file(file_complete_path, input_data)

    return file_complete_path

def get_config_file(problem_code):
    config_list_path = os.path.join(".", "configuration_file_list.json")
    with open(config_list_path, "r") as config_files_list:
        config_files = json.loads(config_files_list.read())
        return config_files[problem_code]


def create_output_directory(input_name):
    directory_name = os.path.join(".", "outputs")
    if (not os.path.isdir(directory_name)):
        os.mkdir(directory_name)
    print("*****************************")
    results_directory_name = input_name.split(".")[0]
    # print(input_name)

    results_directory_path = (
        os.path.join(directory_name, results_directory_name)
    )
    
    # print(results_directory_path)
    if (not os.path.exists(results_directory_path)):
        os.mkdir(results_directory_path)
    else:
        for old_output_result in os.listdir(results_directory_path):
            os.remove(os.path.join(results_directory_path, old_output_result))

    return results_directory_path


def call_solver(input_path, output_path, config_file, time_limit, seed):

    solver_path = "../solver/solver.py"

    command = ""
    command += str(sys.executable) + " "
    command += solver_path + " "
    command += "--input" + " " + str(input_path) + " "
    command += "--output-path" + " " + str(output_path) + " "
    command += "--set-config-file" + " " + str(config_file) + " "
    command += "--set-time-limit" + " " + str(time_limit) + " "
    command += "--set-seed" + " " + str(seed) + " "
    command += "--make-log" + " "
    command += "--detail-solution-log" + " "
    print(command)

    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    exit_code = sp.wait()
    print("exit status:", exit_code)




def run_solver(input_path, config_file, time_limit=300, seed=None):
    
    input_name = os.path.split(input_path)[-1]
    output_path = create_output_directory(input_name)
    solution = call_solver(
        input_path, 
        output_path,
        config_file,
        time_limit,
        seed
    )

