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


    def __init__(self):
        super().__init__("Sartori and Buriol 2020 algorithm")