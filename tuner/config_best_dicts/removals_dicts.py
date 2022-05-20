removal_params = {}

def removal_options(params):
    opts = [("RandomRemoval", "WorstRemoval", "ShawRemovalPDPTW")]
    choice = opts[params["removal_opt"]]
    return choice

def removal_options_dynamic(params):
    opts = [("RandomRemoval", "WorstRemoval", "ShawRemovalPDPTW")]
    choice = opts[params["removal_opt"]]
    return choice

def random_removal(params):
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
        ]
    }

    return data

def random_removal_dynamic(params):
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "FixedRequests"
        ]
    }

    return data



def worst_removal(params):
    global removal_params
    removal_params["p_worst"] = params["p_worst"]
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
        ],
        "p" : removal_params["p_worst"]
    }
    

    return data


def worst_removal_dynamic(params):
    global removal_params
    removal_params["p_worst"] = params["p_worst"]

    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "FixedRequests"
        ],
        "p" : removal_params["p_worst"]
    }
    

    return data


def shaw_removal_PDPTW(params):
    global removal_params
    removal_params["p_shaw"] = params["p_shaw"]
    
    removal_params["phi"] = params["phi"]
    removal_params["qui"] = params["qui"]
    removal_params["psi"] = params["psi"]
    
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
        ],
        "p" : removal_params["p_shaw"],
        "phi" : removal_params["phi"],
        "qui" : removal_params["qui"],
        "psi" : removal_params["psi"]
    }

    return data

def shaw_removal_DPDPTW(params):
    global removal_params
    removal_params["p_shaw"] = params["p_shaw"]
    
    removal_params["phi"] = params["phi"]
    removal_params["qui"] = params["qui"]
    removal_params["psi"] = params["psi"]
    
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
            "FixedRequests"
        ],
        "p" : removal_params["p_shaw"],
        "phi" : removal_params["phi"],
        "qui" : removal_params["qui"],
        "psi" : removal_params["psi"]
    }

    return data


def removal_data(params, problem):

    rr_name = None
    rr = None
    wr_name = None
    wr = None
    sr_name = None
    sr = None

    if (problem == "PDPTW"):
        rr_name = "RandomRemoval"
        rr = random_removal(params)
        wr_name = "WorstRemoval"
        wr = worst_removal(params)
        sr_name = "ShawRemovalPDPTW"
        sr = shaw_removal_PDPTW(params)
    if (
        problem == "DPDPTW" or 
        problem == "DPDPTWLF-R" or 
        problem == "DPDPTWLHF-R"
    ):
        rr_name = "RandomRemoval"
        rr = random_removal_dynamic(params)
        wr_name = "WorstRemoval"
        wr = worst_removal_dynamic(params)
        sr_name = "ShawRemovalDPDPTW"
        sr = shaw_removal_DPDPTW(params)


    algs_data = {
        rr_name : rr,
        wr_name : wr,
        sr_name : sr
    }
    return algs_data
