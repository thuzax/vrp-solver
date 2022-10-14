import os
import sys

import mitrovic_minic_to_json_input_conversor

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Needs input and output dirs")
        exit(0)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    files_names = os.listdir(input_folder)
    print(files_names)

    if (not os.path.exists(output_folder)):
        os.makedirs(output_folder)

    for file_name in files_names:
        f_path = os.path.join(input_folder, file_name)
        print(f_path)
        if (not os.path.isfile(f_path)):
            continue
        args = (f_path, output_folder)
        mitrovic_minic_to_json_input_conversor.convert_file(args)
