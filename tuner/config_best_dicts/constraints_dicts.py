def time_windows_constraint():
    data = {}
    return data

def homogeneous_capacity_constraint():
    data = {}
    return data

def pickup_delivery_constraint():
    data = {}
    return data

def attend_all_requests():
    data = {}
    return data

def fixed_requests():
    data = {}
    return data

def limited_fleet():
    data = {}
    return data

def heterogeneous_fleet():
    data = {}
    return data
    
def constraints_data(params, problem):
    constr_data = {}
    if (problem == "PDPTW"):
        constr_data = {
            "TimeWindowsConstraint" : (
                time_windows_constraint()
            ),
            "HomogeneousCapacityConstraint": (
                homogeneous_capacity_constraint()
            ),
            "PickupDeliveryConstraint": (
                pickup_delivery_constraint()
            ),
            "AttendAllRequests" : attend_all_requests()
        }
    if (problem == "DPDPTW"):
        constr_data = {
            "TimeWindowsConstraint" : (
                time_windows_constraint()
            ),
            "HomogeneousCapacityConstraint": (
                homogeneous_capacity_constraint()
            ),
            "PickupDeliveryConstraint": (
                pickup_delivery_constraint()
            ),
            "AttendAllRequests" : attend_all_requests(),

            "FixedRequests" : fixed_requests()
        }
    if (problem == "DPDPTWLF-R"):
        constr_data = {
            "TimeWindowsConstraint" : (
                time_windows_constraint()
            ),
            "HomogeneousCapacityConstraint": (
                homogeneous_capacity_constraint()
            ),
            "PickupDeliveryConstraint": (
                pickup_delivery_constraint()
            ),
            "AttendAllRequests" : attend_all_requests(),

            "FixedRequests" : fixed_requests(),

            "LimitedFleet" : limited_fleet()    
        }
    if (problem == "DPDPTWNoC-D"):
        constr_data = {
            "TimeWindowsConstraint" : (
                time_windows_constraint()
            ),
            "PickupDeliveryConstraint": (
                pickup_delivery_constraint()
            ),
            "AttendAllRequests" : attend_all_requests(),

            "FixedRequests" : fixed_requests(),

            "LimitedFleet" : limited_fleet()    
        }
    if (problem == "DPDPTWUR-R"):

        constr_data = {
            "TimeWindowsConstraint" : (
                time_windows_constraint()
            ),
            "HomogeneousCapacityConstraint": (
                homogeneous_capacity_constraint()
            ),
            "PickupDeliveryConstraint": (
                pickup_delivery_constraint()
            ),
            "AttendAllRequests" : attend_all_requests(),

            "FixedRequests" : fixed_requests(),

            "LimitedFleet" : limited_fleet(),
            
            "HeterogeneousFleet" : heterogeneous_fleet()
        }
    
    return constr_data
