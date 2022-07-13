import time
import json


make_log = False
solution_detailed = False
start_time = None
log_data = ""
log_solutions_dicts = []

output_path = ""
output_name = ""


def get_log_text():
    global log_data
    return log_data

def get_log_sol_dict():
    global log_solutions_dicts
    return log_solutions_dicts

def set_to_make_log(
    make_log_argument, 
    out_path, 
    out_name, 
    detail_solution=False
):

    global start_time
    start_time = time.time()

    global make_log
    make_log = make_log_argument

    global solution_detailed
    solution_detailed = detail_solution

    global log_data
    log_data += "-" * 80
    
    global output_path
    output_path = out_path
    global output_name
    output_name = out_name
    
    file_name = get_log_file_name()

    with open(file_name, "w") as out:
        pass

    file_json_name = get_solutions_log_file_name()
    
    with open(file_json_name, 'w') as out_json:
        json.dump([], out_json)


    write_text_data(log_data)


def do_file_log():
    global make_log
    return make_log


def detail_solution():
    global solution_detailed
    return solution_detailed


def add_text_to_log_data(text):
    text += "\n"
    global log_data
    
    log_data = text
    log_data += "-" * 80
    
    write_text_data(log_data)

    
def add_dict_to_log_dicts(sol_dict):
    file_name = get_solutions_log_file_name()
    with open(file_name, 'r+') as out:
        out.seek(0, 2)
        position = out.tell() - 1
        out.seek(position)
        if (position <= 1):
            out.write(json.dumps(sol_dict) + "]")
            return
        out.write("," + json.dumps(sol_dict) + "]")


def get_time_text():
    global start_time
    text = "(Solver execution current time: " 
    text += str(time.time() - start_time) + ")" + "\n"
    return text


def add_info_log(message):
    if(not do_file_log()):
        return
    
    text = ""
    text += get_time_text()
    text += "[INFO] "
    text += str(message)
    
    add_text_to_log_data(text)


def add_warning_log(message):
    if(not do_file_log()):
        return
    
    text = ""
    text += get_time_text()
    text += "[WARNING] "
    text += str(message)

    add_text_to_log_data(text)


def add_error_log(message):
    if(not do_file_log()):
        return
    
    text = ""
    text += get_time_text()
    text += "[ERROR]" + "\n"
    text += str(message)

    add_text_to_log_data(text)


def add_solution_log(solution, extra_message=None):
    if (not do_file_log()):
        return

    text = ""
    text += get_time_text()
    text += "[SOLUTION]" + "\n"
    if (extra_message is not None):
        text += extra_message

    text += solution.get_costs_output_text() + "\n"
    
    if (detail_solution()):
        text += solution.get_routes_output_text()
    
    add_text_to_log_data(text)
    add_dict_to_log_dicts(solution.get_dict())


def get_log_file_name():
    if (not do_file_log()):
        return None

    global output_path
    global output_name
    
    if (output_path[-1] != "/"):
        output_path = output_path + "/"


    file_name = output_path + output_name + "_log.txt"
    
    return file_name


def get_solution_data_file_name():
    global output_path
    global output_name
    
    if (output_path[-1] != "/"):
        output_path = output_path + "/"


    file_name = output_path + output_name + "_sol_data.json"
    
    return file_name



def get_solutions_log_file_name():
    if (not do_file_log()):
        return None

    global output_path
    global output_name
    
    if (output_path[-1] != "/"):
        output_path = output_path + "/"


    file_name = output_path + output_name + "_sol_log.json"
    
    return file_name



def write_text_data(data):
    if (not do_file_log()):
        return

    file_name = get_log_file_name()
    with open(file_name, "a") as out:
        out.write(log_data)


def write_sol_json_log(output_path, output_name):
    if (not do_file_log()):
        return

    file_name = get_log_file_name()

    with open(file_name, "w+") as out_file:
        out_file.write(json.dumps(log_solutions_dicts))

def write_solution_data_dict_in_json(solution_data_dict):
    file_name = get_solution_data_file_name()

    with open(file_name, "w+") as out_file:
        out_file.write(json.dumps(solution_data_dict))


    