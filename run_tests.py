
from importlib.metadata import files
import os
import sys
import subprocess
import time

import verify_solution



def verify_all_solutions(
    input_file, 
    input_complete_path,
    output_run_dir, 
    number_of_slices,
    problem
):
    inputs = os.path.join(output_run_dir, "inputs")
    outputs = os.path.join(output_run_dir, "outputs")

    ver_file_name = os.path.join(output_run_dir, "verification.txt")
    with open(ver_file_name, "w") as v:
        pass

    slice_dir = input_file.split(".")[0]
    for i in range(number_of_slices):
        text = ""
        slice_input = input_file.split(".")[0] + "_slice_" + str(i+1) + ".json"
        slice_input_path = os.path.join(inputs, slice_input)
        slice_output = input_file.split(".")[0] + "_slice_" + str(i+1)
        sol_file_name = slice_output + "_sol_log.json"
        slice_output_path = os.path.join(outputs, slice_output, sol_file_name)

        all_sol = "-a"

        text += slice_input + "\n"
        text += verify_solution.verify(
            (slice_input_path, slice_output_path, problem, all_sol)
        )

        with open(ver_file_name, "a") as file_ver:
            file_ver.write(text)

    last_slice_output_path = os.path.join(
        output_run_dir,
        "sr_log",
        input_file.split(".")[0],
        "outputs",
        (
            input_file.split(".")[0] 
            + "_" 
            + str(number_of_slices) 
            + "_sol.json"
        )
    )

    text = "-------------FULL SOLUTION-------------" + "\n"
    text += input_file + "\n"
    text += verify_solution.verify(
        (input_complete_path, last_slice_output_path, problem)
    )

    with open(ver_file_name, "a") as file_ver:
        file_ver.write(text)


if __name__=="__main__":
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
    files_names = files_names[:5]
    
    n_runs = 1

    time_limit = 30

    time_slice = 60
    number_of_slices = 10

    for i in range(n_runs):
        for file_name in files_names:
            print("=" * 80)
            run_name = file_name.split(".")[0] + "_run_" + str(i+1)
            output_run_dir = os.path.join(
                output_dir, 
                run_name
            )

            if (not os.path.exists(output_run_dir)):
                os.makedirs(output_run_dir)
            
            input_file = os.path.join("..", tests_dir, file_name)

            command = ""
            command = str(sys.executable) + " "
            command += "server_requests.py "
            command += "--time-limit " + str(time_limit) + " " 
            command += "--time-slice " + str(time_slice) + " "
            command += "--is-test "
            command += "--test-directly "
            command += "--test-instance " + input_file + " "
            command += "--output-location " 
            command += os.path.join("..", output_run_dir) + " "

            command += "--problem " + problem

            print(command)
            print("-" * 80)
            
            start_time = time.time()
            
            server_requests_dir = os.path.join(".", "server_requests")

            sp = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE,
                cwd=server_requests_dir
            )
            output = sp.communicate()[0]

            exit_code = sp.returncode

            print("EXEC TIME: " + str(time.time() - start_time))

            verify_all_solutions(
                file_name, 
                os.path.join(tests_dir, file_name),
                output_run_dir, 
                number_of_slices,
                problem
            )

            print("=" * 80)
