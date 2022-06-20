import os
import sys

import add_elements_to_instance

if __name__ == "__main__":
    args = sys.argv[1:]
    if (len(args) < 3):
        print("Needs json input dir, output path and problem type")
        exit(0)        

    input_folder = args[0]
    output_folder = args[1]
    problem = args[2]

    orig_fleet = None
    method_code = None

    problem = problem.upper()

    if (problem == "DPDPTW-R"):
        if (len(args) < 4):
            text = "Needs fleet size of classic problem solution"
            print(text)
            exit(0)

        orig_fleet = int(args[3])

    if (problem == "DPDPTWUR-R"):

        if (len(args) < 5):
            text = "Needs \n(1) fleet size of classic problem solution, \n(2)"
            text += " the method for urban and rural division being: \n"
            text += "  CL - clustering\n  CS - center_seeds\n  "
            text += "OC - one clustering\n  DB - dbscan\n  OP - optics)"
            print(text)
            exit(0)

        orig_fleet = int(args[3])
        method_code = args[4]

    files_names = os.listdir(input_folder)

    print(files_names)

    if (not os.path.exists(output_folder)):
        os.makedirs(output_folder)

    for file_name in files_names:
        args = [os.path.join(input_folder, file_name), output_folder, problem]
        if (orig_fleet is not None):
            args.append(orig_fleet)
            if (method_code is not None):
                args.append(orig_fleet)

        add_elements_to_instance.add_elements(args)
