from src.route_classes import *
from src.solvers.SovlerClass import SolverClass

class SartoriBuriolPDPTW(SolverClass):

    points = None
    distance_matrix = None
    time_matrix = None
    capacity = None
    demands = None
    services_times = None
    time_windows = None
    planning_horizon = None
    time_windows_size = None
    origin_id = None
    pickups_ids = None
    deliveries_ids = None
    number_of_requests = None


    def __init__(self):
        super().__init__("Sartori and Buriol 2020 algorithm")

    
    def construct_initial_solution(self):
        solution_routes = []
        
        r = Route()
        print(r.__dict__)
        
        r.insert(self.origin_id)
        
        print(r)
        for pickup in self.pickups_ids:
            delivery = pickup + self.number_of_requests
            r.insert(pickup)
            r.insert(delivery)
            print(r)

        solution_routes.append(r)
        return solution_routes




    def solve(self):
        solution_routes = self.construct_initial_solution()

        for route in solution_routes:
            for v in self.pickups_ids:
                if v in route:
                    route.remove(v)
                    route.remove(v + self.number_of_requests)
                    print(route)
                