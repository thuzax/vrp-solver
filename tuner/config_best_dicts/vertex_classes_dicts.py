def vertex_pdptw():
    v_data = {
    }

    return v_data

def vertex_dpdptw():
    v_data = {
    }

    return v_data

def vertex_dpdptwlhf():
    v_data = {
    }

    return v_data


def vertex_data(params, problem):
    if (problem == "PDPTW"):
        v_data = {
            "VertexPDPTW" : vertex_pdptw(),
        }
    if (
        problem == "DPDPTW" 
        or problem == "DPDPTWLF-R" 
        or problem == "DPDPTWNoC-D"
    ):
        v_data = {
            "VertexDPDPTW" : vertex_dpdptw(),
        }
    if (problem == "DPDPTWLHF-R"):
        v_data = {
            "VertexDPDPTWHeterogeneousFleet" : (
                vertex_dpdptwlhf()
            )
        }

    return v_data
