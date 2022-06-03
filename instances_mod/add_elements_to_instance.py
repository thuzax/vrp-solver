import json
import sys
import os
import fleet_generator
import urban_rural_aptitude_generator


def read_constants():
    
    with open("./constants.json", "r") as constants_file:
        constants = json.loads(constants_file.read())
    
    fleet_generator.correction_value = constants["correction_value"]
    
    urban_rural_aptitude_generator.density_per_min = (
        constants["density_per_min"]
    )

    urban_rural_aptitude_generator.ratio_urban_centers = (
        constants["ratio_urban_centers"]
    )

    urban_rural_aptitude_generator.max_urban_distance = (
        constants["max_urban_distance"]
    )

    urban_rural_aptitude_generator.save_figure = (
        constants["save_figure"]
    )

    urban_rural_aptitude_generator.show_figure = (
        constants["show_figure"]
    )

    urban_rural_aptitude_generator.density_clustering_per_distance = (
        constants["density_clustering_per_distance"]
    )




def get_urb_rural_division_method(method_code):
    method = ""
    if (method_code == "CL"):
        method = "clustering"
    if (method_code == "CS"):
        method = "center_seeds"
    if (method_code == "OC"):
        method = "one_clustering"
    if (method_code == "DB"):
        method = "dbscan"
    if (method_code == "OP"):
        method = "optics"
    return method



def read_file(input_file_name):
    with open(input_file_name, "r") as input_file:
        data = json.loads(input_file.read())

    return data


def get_destiny_folder(input_name, problem):
    directory_name = os.path.split(input_name)[-1].split(".")[0]
    directory_name += "_" + problem
    
    if (not os.path.isdir(directory_name)):
        os.mkdir(directory_name)

    return directory_name


def get_out_file_name(input_file, problem):
    input_name = os.path.split(input_file)[-1]
    input_name = problem + "_" + input_name
    return input_name


if __name__ == "__main__":

    if (len(sys.argv) < 4):
        print("Needs json input file, output path and problem type")
        exit(0)        

    read_constants()

    input_file_name = sys.argv[1]
    output_file_path = sys.argv[2]

    if (not os.path.exists(output_file_path)):
        os.makedirs(output_file_path)

    data = read_file(input_file_name)

    problem = sys.argv[3]

    if (problem == "DPDPTW"):
        data["fixed"] = {}

        directory_name = output_file_path
        out_name = get_out_file_name(input_file_name, problem)
        out_path = os.path.join(directory_name, out_name)

        with open(out_path, "w") as out_file:
            out_file.write(json.dumps(data))

    if (problem == "DPDPTW-R"):
        if (len(sys.argv) < 5):
            text = "Needs fleet size of classic problem solution"
            print(text)
            exit(0)

        orig_fleet = int(sys.argv[4])

        fleet = fleet_generator.generate_fleet_size(orig_fleet)
        print(fleet)

        data["fleet_size"] = fleet
        data["fixed"] = {}
        
        print(input_file_name)
        directory_name = output_file_path
        out_name = get_out_file_name(input_file_name, problem)

        out_path = os.path.join(directory_name, out_name)
        with open(out_path, "w") as out_file:
            out_file.write(json.dumps(data))


    if (problem == "DPDPTWUR-R"):

        if (len(sys.argv) < 6):
            text = "Needs \n(1) fleet size of classic problem solution, \n(2)"
            text += " the method for urban and rural division being: \n"
            text += "  CL - clustering\n  CS - center_seeds\n  "
            text += "OC - one clustering\n  DB - dbscan\n  OP - optics)"
            print(text)
            exit(0)

        orig_fleet = int(sys.argv[4])
        method_code = sys.argv[5]

        method = get_urb_rural_division_method(method_code)
        points = [0 for i in range(len(data["points"]))]
        for key, value in data["points"].items():
            points[int(key)] = tuple(value)
        

        figure_path = output_file_path
        figure_name = get_out_file_name(input_file_name, problem)


        urb_rural_apt = urban_rural_aptitude_generator.get_urb_rural_division(
            points,
            method,
            figure_path,
            figure_name
        )


        fleet = fleet_generator.generate_urb_rur_fleet(
            orig_fleet, 
            urb_rural_apt
        )
        print("u:", len([i for i in urb_rural_apt if i == 0]))
        print("r:", len([i for i in urb_rural_apt if i == 1]))
        print(fleet)
        data["fleet"] = []
        
        for key, value in fleet.items():
            data["fleet"]. append([value, list(key)])
        
        data["attendance_type"] = {
            key : value
            for key, value in enumerate(urb_rural_apt)
        }

        data["fixed"] = {}


        directory_name = output_file_path
        out_name = get_out_file_name(input_file_name, problem+"_"+method)
        out_path = os.path.join(directory_name, out_name)
        with open(out_path, "w") as out_file:
            out_file.write(json.dumps(data))

        