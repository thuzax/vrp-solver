
import hyperopt
from tuner_src import params_constructives

solver_params = {}

def get_params_dict():
    global solver_params
    return solver_params

def solvers_options(problem):
    choice = None
    if (problem == "PDPTW"):
        choice = hyperopt.hp.choice(
            "solver_choice",
            [
                "SolverPDPTW"
            ]
        )
    if (problem == "DPDPTW" or problem == "DPDPTWLF-R"):
        choice = hyperopt.hp.choice(
            "solver_choice",
            [
                "SolverDPDPTW"
            ]
        )
    if (problem == "DPDPTWLHF-R"):
        choice = hyperopt.hp.choice(
            "solver_choice",
            [
                "SolverDPDPTWHeterogeneousFleet"
            ]
        )
    
    solver_params["solver_choice"] = choice
    
    return choice


def solver_pdptw():
    data  = {
        "output_type" : "json",
        "obj_func_name" : "ObjVehiclePDPTW",
        "construction_name" : "BasicGreedy",
        "metaheuristic_name" : "SBMath",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "PickupDeliveryConstraint",
            "AttendAllRequests"
        ]
    }
    
    return data


def solver_dpdptw():
    data  = {
        "output_type" : "json",
        "obj_func_name" : "ObjVehiclePDPTW",
        "construction_name" : "BasicGreedy",
        "metaheuristic_name" : "SBMath",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "PickupDeliveryConstraint",
            "FixedRequests",
            "AttendAllRequests"
        ]
    }
    
    return data



def solver_pdptwlfr():
    data  = {
        "output_type" : "json",
        "obj_func_name" : "ObjRequestsPDPTW",
        "construction_name" : "BasicGreedyLimitedFleet",
        "metaheuristic_name" : "SBMath",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "PickupDeliveryConstraint",
            "FixedRequests",
            "LimitedFleet"
        ]
    }
    
    return data

def solver_pdptwlhfr():
    data  = {
        "output_type" : "json",
        "obj_func_name" : "ObjRequestsPDPTW",
        "construction_name" : "BasicGreedyLimitedHeterogeneousFleet",
        "metaheuristic_name" : "SBMath",
        "constraints_names" : [
            "HomogeneousCapacityConstraint",
            "TimeWindowsConstraint",
            "PickupDeliveryConstraint",
            "FixedRequests",
            "LimitedFleet",
            "HeterogeneousFleet"
        ]
    }
    
    return data