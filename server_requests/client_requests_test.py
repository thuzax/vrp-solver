import sys
import requests
import random
import json

def get_base_link():
    return "http://127.0.0.1:6969/"

def create_pairs(n):
    pairs = set()
    for i in range(1, n+1):
        pair = (i, i + n)
        pairs.add(pair)

    return pairs


def make_requests_dicts(input_file):
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
        requests_dicts.append(request_dict)
        
    return requests_dicts


def send_request(request_dict):
    link = get_base_link() + "make_request"
    json_data = json.dumps(request_dict)
    print(json_data)
    r = requests.post(link, json=json_data, timeout=60)
    return r

def send_requests(requests_dicts):
    for request in requests_dicts:
        result = send_request(request)
        print(result.text)


if __name__=="__main__":
    if (len(sys.argv) < 2):
        print("Input needed")
        exit(0)
    
    input_name = sys.argv[1]
    requests_dicts = make_requests_dicts(input_name)

    for k in range(1):
        i = 3
        for j in range(int(len(requests_dicts)/i)):
            start = j * i
            end = (j + 1) * i
            print("SENDING", start, "TO", end-1)
            send_requests(requests_dicts[start:end])
        
        last = (int(len(requests_dicts) / i) * i)
        print("SENDING REMAINING (IF THERE ARE)")


        if (last < len(requests_dicts)):
            send_requests(requests_dicts[last:])
    


