import time

make_log = False
solution_detailed = False
start_time = None
log_data = ""


def set_to_make_log(make_log_argument, detail_solution=False):
    global start_time
    start_time = time.time()

    global make_log
    make_log = make_log_argument

    global solution_detailed
    solution_detailed = detail_solution
    global log_data
    log_data += "-" * 80


def do_file_log():
    global make_log
    return make_log


def detail_solution():
    global solution_detailed
    return solution_detailed


def add_text_to_log_data(text):
    text += "\n"
    global log_data
    log_data += text
    log_data += "-" * 80


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
    text += message
    
    add_text_to_log_data(text)


def add_warning_log(message):
    if(not do_file_log()):
        return
    
    text = ""
    text += get_time_text()
    text += "[WARNING] "
    text += message

    add_text_to_log_data(text)


def add_error_log(message):
    if(not do_file_log()):
        return
    
    text = ""
    text += get_time_text()
    text += "[ERROR]" + "\n"
    text += message

    add_text_to_log_data(text)


def add_solution_log(solution, extra_message=None):
    if (not do_file_log()):
        return

    text = ""
    text += get_time_text()
    text += "[SOLUTION]" + "\n"
    if (extra_message is not None):
        text += extra_message

    text += solution.get_costs_output() + "\n"
    
    if (detail_solution()):
        text += solution.get_routes_output()
    
    add_text_to_log_data(text)


def write_log(output_path, output_name):
    if (not do_file_log()):
        return
    if (output_path[-1] != "/"):
        output_path = output_path + "/"

    output_name = output_name + "_log.txt"
    with open(output_path + output_name, "w") as out_file:
        out_file.write(log_data)