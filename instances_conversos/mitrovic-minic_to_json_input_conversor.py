import sys
import json
import os
import pprint

def euclidian(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]

    result = (x**2 + y**2)**(1/2)

    # result = round(result, 1)
    # Distancia em hectometros
    result = int(result)

    return result

def calculate_travel_time(distance):
    # vehicle_speed = 1 # 1 km/minuto = 60 km/h
    vehicle_speed = 10 # 10 hectometro/minuto = 1 km/minuto = 60 km/h
    travel_time = distance/vehicle_speed
    return int(travel_time)
    # return int(round(travel_time))

if __name__=="__main__":
    file_name = sys.argv[1]
    out_path = "./"
    if (len(sys.argv) == 3):
        out_path = sys.argv[2]

    with open(file_name, "r") as input_file:
        text = input_file.read()
        lines = text.split("\n")
        lines = [line for line in lines if line != ""]
        
        json_file_name = file_name.strip().split("/")[-1]
        json_file_name = "mitrovic-minic_" + json_file_name.strip().split(".")[0] + ".json"
        
        number_of_requests = len(lines) - 4
        plan_horizon = os.path.basename(file_name).split(".")[0].split("_")[1]
        plan_horizon = int(plan_horizon[:-1]) * 60

        tws_size = None

        capacity = 1

        lines = lines[4:]

        points = {}
        demands = {}
        tws = {}
        services_times = {}
        pairs = set()

        pickups = set()
        deliveries = set()

        old_pairs = {}

        pairs = set()

        for i in range(number_of_requests):
            line = lines[i].strip().split()
            if (len(line) == 0):
                continue
            idx = int(line[0])+1
            

            if (int(idx) != 0):
                pick = idx
                deli = idx+number_of_requests
                pickups.add(idx)
                deliveries.add(deli)    
                pairs.add((pick, deli))
        pickups = tuple(pickups)
        deliveries = tuple(deliveries)

        # points[0] = (20, 30)
        points[0] = (20*10, 30*10)

        requests_times_in = {}

        for i in range(number_of_requests):
            line = lines[i].strip().split()
            if (len(line) == 0):
                continue

            pick = i+1
            
            # Transformando km em hectometro para excluir vírgulas
            # points[pick] = [float(line[3]), float(line[4])]
            points[pick] = [int(float(line[3])*10), int(float(line[4])*10)]

            demands[pick] = 0
            
            tws[pick] = [int(line[5]), int(line[6])]
            services_times[pick] = int(line[2])

            deli = pick + number_of_requests

            # Transformando km em hectometro para excluir vírgulas
            # points[deli] = [float(line[8]), float(line[9])]
            points[deli] = [int(float(line[8])*10), int(float(line[9])*10)]
            
            demands[deli] = 0
            
            tws[deli] = [int(line[10]), int(line[11])]
            services_times[deli] = int(line[7])
            
            requests_times_in[(pick, deli)] = int(line[1])

            # print(
            #     i,
            #     requests_times_in[(pick, deli)],
            #     services_times[pick],
            #     points[pick],
            #     tws[pick], 
            #     services_times[deli],
            #     points[deli],
            #     tws[deli]
            # )
        
        pairs = [list(pair) for pair in pairs]

        distance_matrix = {}
        for i in range(number_of_requests*2+1):
            distance_matrix[i] = {}
            for j in range(number_of_requests*2+1):
                if (i == j):
                    distance_matrix[i][j] = 0
                    continue
                distance_matrix[i][j] = euclidian(points[i], points[j])
    
        time_matrix = {}
        for i in range(number_of_requests*2+1):
            time_matrix[i] = {}
            for j in range(number_of_requests*2+1):
                if (i == j):
                    time_matrix[i][j] = 0
                    continue
                time_matrix[i][j] = calculate_travel_time(distance_matrix[i][j])
        
        file_dict = {}

        file_dict["points"] = points
        file_dict["number_of_points"] = number_of_requests*2+1
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
