def route_pdptw():
    r_data = {
    }

    return r_data


def route_dpdptw():
    r_data = {
    }

    return r_data



def route_dpdptwlhf():
    r_data = {
    }

    return r_data

def route_data(params, problem):
    if (problem == "PDPTW"):
        r_data = {
            "RoutePDPTW" : route_pdptw(),
        }
    if (problem == "DPDPTW" or problem == "DPDPTWLF-R"):
        r_data = {
            "RouteDPDPTW" : route_dpdptw(),
        }
    if (problem == "DPDPTWLHF-R"):
        r_data = {
            "RouteDPDPTWHeterogeneousFleet" : route_dpdptwlhf()
        }

    return r_data