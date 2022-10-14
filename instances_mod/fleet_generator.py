import numpy
import random
import math
import collections


correction_value = None

def divide_fleet(fleet_size, urban_rural_aptitude):
    repetitions = collections.Counter(urban_rural_aptitude)

    number_urban_clients = repetitions[0]
    number_rural_clients = repetitions[1]

    rural_ratio = (
        number_rural_clients / 
        len(urban_rural_aptitude)
    )


    rural_fleet_size = math.ceil(
                        rural_ratio
                        * (fleet_size * correction_value)
                    )
    urban_fleet_size = math.ceil(
                        fleet_size -
                        rural_ratio
                        * (fleet_size * correction_value)
                    )

    return {
        (0,): urban_fleet_size, 
        (0,1): rural_fleet_size
    }
    

def generate_fleet_size(n_vehicles_solution):
    fleet_size = math.ceil(
        n_vehicles_solution
    )
    return fleet_size


def generate_urb_rur_fleet(n_vehicles_solution, urb_rural_apt):
    fleet_size = generate_fleet_size(n_vehicles_solution)

    fleets_sizes = divide_fleet(fleet_size, urb_rural_apt)

    return fleets_sizes
