import sys
import json


def euclidian(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]

    result = (x**2 + y**2)**(1/2)
    return result

if __name__=="__main__":
    file_name = sys.argv[1]
    out_path = "./"
    if (len(sys.argv) == 3):
        out_path = sys.argv[2]

    with open(file_name, "r") as input_file:
        text = input_file.read()
        lines = text.split("\n")
        
        json_file_name = file_name.strip().split("/")[-1]
        json_file_name = "li_lim_" + json_file_name.strip().split(".")[0] + ".json"
        
        number_of_points = len(lines) - 2

        plan_horizon = int(lines[1].strip().split()[5])

        tws_size = None

        capacity = int(lines[0].strip().split()[1])

        lines = lines[1:]

        points = {}
        demands = {}
        tws = {}
        services_times = {}
        pairs = set()

        pickups = set()
        deliveries = set()

        old_pairs = {}


        for i in range(number_of_points):
            line = lines[i].strip().split()
            if (len(line) == 0):
                continue
            idx = int(line[0])

            if (int(idx) != 0):
                pick = int(line[7])
                deli = int(line[8])

                if (pick == 0 and deli != 0):
                    deliveries.add(deli)
                    pickups.add(idx)
                    old_pairs[idx] = deli
                
                if (pick != 0 and deli == 0):
                    pickups.add(pick)
                    deliveries.add(idx)
                    old_pairs[idx] = pick
                    

        pickups = tuple(pickups)
        deliveries = tuple(deliveries)

        old_id_to_new = {}
        new_id_to_old = {}
        
        pairs = set()
        
        for i, pickup in enumerate(pickups):
            
            new_pick_id = i+1
            new_deli_id = new_pick_id + int((number_of_points-1)/2)
            
            old_id_to_new[pickup] = new_pick_id
            new_id_to_old[new_pick_id] = pickup
            
            deli_old_id = old_pairs[pickup]
            
            old_id_to_new[deli_old_id] = new_deli_id
            new_id_to_old[new_deli_id] = deli_old_id
            
            pairs.add((new_pick_id, new_deli_id))


        old_id_to_new[0] = 0
        new_id_to_old[0] = 0


        for i in range(number_of_points):
            line_pos = new_id_to_old[i]
            line = lines[line_pos].strip().split()
            if (len(line) == 0):
                continue

            idx = i
            points[idx] = [float(line[1]), float(line[2])]
            
            if (idx != 0):

                demands[idx] = int(line[3])
                tws[idx] = [int(line[4]), int(line[5])]
                services_times[idx] = int(line[6])
                
        pairs = [list(pair) for pair in pairs]


        time_matrix = {}
        for i in range(number_of_points):
            time_matrix[i] = {}
            for j in range(number_of_points):
                if (i == j):
                    time_matrix[i][j] = 0
                    continue
                time_matrix[i][j] = euclidian(points[i], points[j])
        
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

        print("ouput: ", out_path + json_file_name)
        with open(out_path + json_file_name, "w+") as output_file:
            output_file.write(json.dumps(file_dict))
            # output_file.write(json.dumps(file_dict, indent=2))