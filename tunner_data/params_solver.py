
import hyperopt
from tunner_data import params_constructives

solver_params = {}

def get_params_dict():
    global solver_params
    return solver_params

def solvers_options():
    choice = hyperopt.hp.choice(
        "solver_choice",
        [
            "SolverPDPTW"
        ]
    )
    
    solver_params["solver_choice"] = choice
    
    return choice


def solver_pdptw():
    data  = {
        "output_type" : "json",
        "obj_func_name" : "ObjVehicles",
        "construction_name" : params_constructives.constructive_options(),
        "metaheuristic_name" : "SBMath",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "PickupDeliveryConstraint",
            "AttendAllRequests"
        ]
    }
    
    return data