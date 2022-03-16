import multiprocessing
import subprocess
import time

import func_timeout
import random


def run(i):
    sp = subprocess.Popen("python3 ./solver.py --input ./test_instances/input_files/SB_json/bar-n100-1_fixed_limited_heter_fleet.json  --output ./test_parallel/t"+str(i)+".json --set-config-file ./configuration-dynamic-obj-request-urb-rur.json --make-log --detail-solution-log --set-seed 0 --set-time-limit 60", shell=True, stdout=subprocess.PIPE)
    exit_code = sp.wait()
    print("exit status:", exit_code)

if __name__ == '__main__':
    print("number of processors:", multiprocessing.cpu_count())
    number_of_process = 5
    print("number of process:", number_of_process)
    sema = multiprocessing.Semaphore(number_of_process)
    all_processes = []
    start_time = time.time()
    for i in range(number_of_process):
        p = multiprocessing.Process(target=run, args=(i,))
        all_processes.append(p)
        # the following line won't block after 20 processes
        # have been created and running, instead it will carry 
        # on until all 1000 processes are created.
        p.start()

    # inside main process, wait for all processes to finish
    for p in all_processes:
        p.join()

    end_time = time.time()
    print("total time: ", end_time - start_time)