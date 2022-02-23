def calculate_requests_total_cost(solution, obj_func):
    obj_requests_cost = 0
    for route in solution.routes():
        for request in route.requests():
            obj_requests_cost += (
                obj_func.get_request_cost_in_route(
                    route, 
                    route.index(request),
                    request
                )
            )
            
    return obj_requests_cost


def calculate_routes_total_cost(solution, obj_func):
    routes_obj_value = 0
    for route in solution.routes():
        routes_obj_value += obj_func.get_route_cost(route) 
    return routes_obj_value


def constraints_check(solution, constraints):
    for constraint in constraints:
        if (not constraint.solution_is_feasible(solution)):
            return False
    return True


def objective_function_value_check(solution, obj_func):
    obj_value = obj_func.get_solution_cost(solution)
    if (obj_value != solution.cost()):
        return False

    return True

def routes_total_value_check(solution, obj_func):
    routes_obj_value = calculate_routes_total_cost(solution, obj_func)
    if (routes_obj_value != solution.routes_cost()):
        return False
    return True


def requests_costs_check(solution, obj_func):
    requests_cost = 0
    for request_cost in solution.requests_costs().values():
        requests_cost += request_cost

    obj_requests_cost = (
        calculate_requests_total_cost(solution, obj_func)
    )

    route_total_cost = calculate_routes_total_cost(solution, obj_func)
    if (obj_requests_cost != requests_cost):
        return False

    return True


def solution_check(solution, constraints, obj_func):
    solution_ok = (
        constraints_check(solution, constraints)
        and objective_function_value_check(solution, obj_func)
        and requests_costs_check(solution, obj_func)
    )
    
    return solution_ok



def get_solution_check_complete_data(solution, constraints, obj_func):
    text = ""
    text += "====================================" + "\n"
    text += "Constraints verification: " + "\n"
    for constraint in constraints:
        if (constraint.solution_is_feasible(solution)):
            text += constraint.name + " OK" + "\n"
        else:
            text += constraint.name + " NOT OK FOR THESE ROUTES" + "\n"
            for route in solution.routes():
                if (not constraint.route_is_feasible(route)):
                    text += str(route) + "\n"

    text += "====================================" + "\n"

    text += "Obj Func verification: " + "\n"
    
    obj_value = obj_func.get_solution_cost(solution)
    
    if (obj_value == solution.cost()):
        text += "SOLUTION COST OK" + "\n"
    else:
        text += "SOLUTION COST NOT OK:" + "\n"
        text += str(solution.cost()) + "\n"
        text += str(obj_value) + "\n"
    text += "------------------------------------" + "\n"
    
    
    routes_obj_value = calculate_routes_total_cost(solution, obj_func)
    
    if (routes_obj_value == solution.routes_cost()):
        text += "ROUTES TOTAL COST OK" + "\n"
    else:
        text += "ROUTES TOTAL COST NOT OK:" + "\n"
        text += str(solution.routes_cost()) + "\n"
        text += str(routes_obj_value) + "\n"
    text += "------------------------------------" + "\n"

    requests_cost = 0
    for request_cost in solution.requests_cost_dict.values():
        requests_cost += request_cost
    
    obj_requests_cost = (
        calculate_requests_total_cost(solution, obj_func)
    )

    if (obj_requests_cost == requests_cost):
        text += "REQUESTS TOTAL COST OK" + "\n"
    else:
        text += "REQUESTS TOTAL COST NOT OK:" + "\n"
        text += str(obj_requests_cost) + "\n"
        text += str(requests_cost) + "\n"
    text += "------------------------------------" + "\n"

    return text