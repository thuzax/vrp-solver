def route_pdptw():
    r_data = {
    }

    return r_data


def route_dpdptwlhf():
    r_data = {
    }

    return r_data

def route_data(params, problem):
    if (problem == "PDPTW" or problem == "DPDPTW" or problem == "DPDPTWLF-R"):
        r_data = {
            "RoutePDPTW" : route_pdptw(),
        }
    if (problem == "DPDPTWLHF-R"):
        r_data = {
            "RoutePDPTWHeterogeneousFleet" : route_dpdptwlhf()
        }

    return r_data