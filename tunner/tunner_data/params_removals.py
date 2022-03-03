import hyperopt

removal_params = {}


def get_params_dict():
    global removal_params
    return removal_params

def removal_options():
    choice = hyperopt.hp.choice(
        "removal_opt",
        [("RandomRemoval", "WorstRemoval", "ShawRemovalPDPTW")]
    )

    global removal_params
    removal_params["removal_opt"] = choice
    
    return choice


def random_removal():
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
        ]
    }

    return data


def worst_removal():
    global removal_params
    removal_params["p_worst"] = hyperopt.hp.choice(
        "p_worst", 
        [i for i in range(11)]
    )
    data = {
        "obj_func_name" : "ObjDistancePDPTW",
        "constraints_names" : [
        ],
        "p" : removal_params["p_worst"]
    }
    

    return data


def shaw_removal_PDPTW():
    global removal_params
    removal_params["p_shaw"] = hyperopt.hp.choice(
        "p_shaw", 
        [i for i in range(11)]
    )
    
    removal_params["phi"] = hyperopt.hp.choice("phi", [i for i in range(11)])
    removal_params["qui"] = hyperopt.hp.choice("qui", [i for i in range(11)])
    removal_params["psi"] = hyperopt.hp.choice("psi", [i for i in range(11)])
    
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
