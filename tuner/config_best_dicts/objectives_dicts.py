def obj_distance_PDPTW(): 
    data = {}
    return data

def obj_vehicles(): 
    data = {}
    return data

def obj_requests_PDPTW(): 
    data = {}
    return data

def objectives_data(params, problem):
    obj_data = {
        "ObjDistancePDPTW" : obj_distance_PDPTW(),
        "ObjVehiclePDPTW" : obj_vehicles(),
        "ObjRequestsPDPTW" : obj_requests_PDPTW()
    }
    
    return obj_data
