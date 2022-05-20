import sys
import json


if __name__=="__main__":

    if (len(sys.argv) < 3):
        print("Needs input file and output location")
        exit(0)

    file_name = sys.argv[1]
    out_path = "./"
    if (len(sys.argv) == 3):
        out_path = sys.argv[2]

    with open(file_name, "r") as input_file:
        text = input_file.read()
        lines = text.split("\n")
        
        json_file_name = lines[0].strip().split(":")[1]
        json_file_name = "SB_" + json_file_name.strip().split(" ")[0] + ".json"
        
        number_of_points = lines[4].strip().split(":")[1]
        number_of_points = int(number_of_points.strip().split(" ")[0])

        plan_horizon = lines[7].strip().split(":")[1]
        plan_horizon = int(plan_horizon.strip().split(" ")[0])

        tws_size = lines[8].strip().split(":")[1]
        tws_size = int(tws_size.strip().split(" ")[0])

        capacity = lines[9].strip().split(":")[1]
        capacity = int(capacity.strip().split(" ")[0])

        lines = lines[11:]

        points = {}
        demands = {}
        tws = {}
        services_times = {}
        pairs = set()


        for i in range(number_of_points):
            line = lines[i].strip().split(" ")

            idx = line[0]

            points[idx] = [float(line[1]), float(line[2])]

            if (int(idx) != 0):
                demands[idx] = int(line[3])
                tws[idx] = [int(line[4]), int(line[5])]
                
                services_times[idx] = int(line[6])
            
                pick = int(line[7])
                deli = int(line[8])
                if (pick == 0 and deli != 0):
                    pairs.add((int(idx), deli))
                if (pick != 0 and deli == 0):
                    pairs.add((pick, int(idx)))
        
        pairs = [list(pair) for pair in pairs]


        lines = lines[number_of_points+1:]

        time_matrix = {}
        for i in range(number_of_points):
            time_matrix[i] = {}
            line = lines[i].strip().split(" ")
            for j in range(number_of_points):
                time_matrix[i][j] = int(line[j])
        
        # TEMPORARIO
        distance_matrix = time_matrix

        file_dict = {}

        file_dict["points"] = points
        file_dict["number_of_points"] = number_of_points
        file_dict["depot"] = 0
        
        file_dict["distance_matrix"] = distance_matrix
        file_dict["time_matrix"] = time_matrix
        
        file_dict["capacity"] = capacity
        file_dict["pickups_and_deliveries"] = pairs
        
        file_dict["demands"] = demands
        file_dict["services_times"] = services_times
        
        file_dict["time_windows_pd"] = tws

        file_dict["planning_horizon"] = plan_horizon
        file_dict["time_windows_size"] = tws_size

        with open(out_path + json_file_name, "w+") as output_file:
            output_file.write(json.dumps(file_dict))
            # output_file.write(json.dumps(file_dict, indent=2))
        print(out_path + json_file_name)
