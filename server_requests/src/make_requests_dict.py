import sys
import requests
import random
import json


def make_requests_dicts(input_file, problem):
    with open(input_file, "r") as inp_f:
        data = inp_f.read()
        data = json.loads(data)
    
    requests_dicts = []
    n_req = int(data["number_of_points"]/2)
    for i in range(n_req):
        pickup = i+1
        delivery = pickup+n_req
        pair = (pickup, delivery)
        request_dict = {}
        
        request_dict["request"] = pair
        request_dict["points"] = (
            data["points"][str(pickup)],
            data["points"][str(delivery)]
        )
        
        request_dict["demands"] = (
            data["demands"][str(pickup)],
            -data["demands"][str(delivery)]
        )
        
        request_dict["services_times"] = (
            data["services_times"][str(pickup)],
            -data["services_times"][str(delivery)]
        )

        request_dict["time_windows"] = (
            data["time_windows_pd"][str(pickup)],
            data["time_windows_pd"][str(delivery)]
        )
        
        if ("times_in" in data):
            request_dict["time_in"] = data["times_in"][str(i+1)]

        if (problem.upper() == "DPDPTWUR-R"):
            request_dict["attendance_type"] = (
                data["attendance_type"][str(pickup)],
                data["attendance_type"][str(delivery)]
            )

        requests_dicts.append(request_dict)
        
    return requests_dicts
