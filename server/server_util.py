import json 
import os
import sys
import subprocess
import multiprocessing
import time


def get_input_file_path(func_code, file_name):
    inputs_directory_path = os.path.join(".", "inputs")
    if not os.path.exists(inputs_directory_path):
        os.mkdir(inputs_directory_path)
    file_complete_path = os.path.join(
        inputs_directory_path, str(func_code) + "_" + str(file_name)
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
        print(config_files[problem_code])
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
    
    return exit_code



def read_solution(output_path, input_name):

    all_solutions = read_all_solutions(output_path, input_name)

    if (all_solutions is None):
        return None
    
    best_solution = all_solutions[-1]
    return best_solution


def read_all_solutions(output_path, input_name):
    input_without_type = input_name.split(".")[0]
    solutions_file_name = input_without_type + "_sol_log.json"
    
    file_solutions = os.path.join(output_path, solutions_file_name)
    
    with open(file_solutions, "r") as all_solutons_file:        
        all_solutions = json.loads(all_solutons_file.read())
        if (len(all_solutions) == 0):
            return None

        return all_solutions

    return None
    


def run_solver(
    input_path, 
    config_file, 
    time_limit=300, 
    seed=None, 
    saved_solutions=False
):
    
    input_name = os.path.split(input_path)[-1]
    output_path = create_output_directory(input_name)
    exit_code = call_solver(
        input_path, 
        output_path,
        config_file,
        time_limit,
        seed
    )

    if (exit_code != 0):
        return None
    
    if (saved_solutions):
        return read_all_solutions(output_path, input_name)

    solution = read_solution(output_path, input_name)
    return solution


def solve_problem(
    problem_code, 
    data, 
    result_storage_arr=None, 
    position_storage=None
):
    input_path = create_input_file(problem_code, data)    
    config_file = get_config_file(problem_code)
    
    time_limit = None
    if ("time_limit" in data.keys()):
        time_limit = data["time_limit"]

    seed = None
    if ("seed" in data.keys()):
        seed = data["seed"]

    saved_solutions = False
    if ("get_all_solutions" in data.keys()):
        saved_solutions = data["get_all_solutions"]

    result = run_solver(
        input_path, 
        config_file, 
        time_limit, 
        seed, 
        saved_solutions
    )

    if (result_storage_arr is not None):
        result_storage_arr[position_storage] = result
    

    if (result is None):
        return "No solution found. Timeout."
    
    return result

def solve_problems_parallel(problem_code, all_inputs_data):
    print("number of processors:", multiprocessing.cpu_count())
    number_of_process = len(all_inputs_data)
    print("number of process:", number_of_process)
    sema = multiprocessing.Semaphore(number_of_process)
    
    start_time = time.time()
    all_processes = []
    manager = multiprocessing.Manager()
    result_storage_arr = manager.list()
    for i, input in enumerate(all_inputs_data):
        result_storage_arr.append(None)
        p = multiprocessing.Process(
            target=solve_problem, 
            args=(problem_code, input, result_storage_arr, i,)
        )
        all_processes.append(p)

        p.start()

    # inside main process, wait for all processes to finish
    for p in all_processes:
        p.join()
    
    for i in range(number_of_process):
        if (result_storage_arr is None):
            result_storage_arr[i] = (
                "No solution found. Probably an error ocurred."
            )
    
    end_time = time.time()
    print("total time: ", end_time - start_time)

    return list(result_storage_arr)