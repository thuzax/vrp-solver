
import hyperopt
from tuner_src import params_constructives

solver_params = {}

def solvers_options(params, problem):
    choice = None
    if (problem == "PDPTW"):
        opts = ["SolverPDPTW"]
    if (problem == "DPDPTW" or problem == "DPDPTWLF-R"):
        opts = ["SolverDPDPTW"]
    if (problem == "DPDPTWLHF-R"):
        opts = ["SolverDPDPTWHeterogeneousFleet"]
    
    choice = opts[params["solver_choice"]]
    solver_params["solver_choice"] = choice
    
    return choice


def solver_pdptw(params):
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


def solver_dpdptw(params):
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


def solver_dpdptw_no_cap(params):
    data  = {
        "output_type" : "json",
        "obj_func_name" : "ObjDistancePDPTW",
        "construction_name" : "BasicGreedyLimitedFleet",
        "metaheuristic_name" : "SBMath",
        "constraints_names" : [
            "TimeWindowsConstraint",
            "PickupDeliveryConstraint",
            "FixedRequests",
            "AttendAllRequests",
            "LimitedFleet"
        ]
    }
    
    return data


def solver_pdptwlfr(params):
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

def solver_pdptwlhfr(params):
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

def solvers_data(params, problem):
    if (problem == "PDPTW"):
        sol_algs = {
            "SolverPDPTW" : solver_pdptw(params)
        }
    
    if (problem == "DPDPTW"):
        sol_algs = {
            "SolverDPDPTW" : solver_dpdptw(params)
        }

    if (problem == "DPDPTWLF-R"):
        sol_algs = {
            "SolverDPDPTW" : solver_pdptwlfr(params)
        }
    
    if (problem == "DPDPTWNoC-D"):
        sol_algs = {
            "SolverDPDPTW" : solver_dpdptw_no_cap(params)
        }

    if (problem == "DPDPTWLHF-R"):
        sol_algs = {
            "SolverDPDPTWHeterogeneousFleet" : solver_pdptwlhfr(params)
        }
    
    return sol_algs
