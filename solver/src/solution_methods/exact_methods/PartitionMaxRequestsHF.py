from mip import *
from src import file_log
from src.route_classes import Route
from src.solution_classes import Solution
from src.solution_methods import PartitionMaxRequests

class PartitionMaxRequestsHF(PartitionMaxRequests):
    def __init__(self):
        super().__init__()
        self.name = "PartitionMaxRequestsHF"

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.vertices = None


    # def create_variables(self, model, parameters):
    #     super().create_variables(model, parameters)
    #     routes_pool = parameters["routes_pool"]
    #     z = [
    #         model.add_var(
    #             var_type=BINARY,
    #             name="z_"+str(i)+","+str(j)
    #         )
    #         for j in self.fleet.keys()
    #         for i in range(len(routes_pool))
    #     ]

    #     return model.vars
        
    
    # def get_variables_start_value(self, model, solution, parameters):
    #     x_y = super().get_variables_start_value(model, solution, parameters)
    #     routes_pool = parameters["routes_pool"]
    #     z = [
    #         [
    #             model.var_by_name("z_"+str(i)+","+str(j)) 
    #             for j in self.fleet.keys()
    #         ]
    #         for i in range(len(routes_pool))
    #     ]
    #     for route_sol in solution.routes():
    #         route_fleet_type = 0
    #         for fleet_type, fleet_data in self.fleet.items():
    #             if (
    #                 route_sol.get_attendance_type() 
    #                 == fleet_data["types"]
    #             ):
    #                 route_fleet_type = fleet_type
            
    #         for i, route in enumerate(routes_pool):
    #             if (route.is_equal(route_sol)):
    #                 z[i][route_fleet_type] = 1
    #                 break
        

                

    def initialize_model(self, model, solution, parameters):
        model.start = self.get_variables_start_value(
            model, 
            solution, 
            parameters
        )

    
    def get_routes_attended_by_vehicle_type(self, routes_pool):
        # O QUE DEVERIA MUDAR AQUI
        routes_by_type = {}
        for i, route in enumerate(routes_pool):
            routes_by_type[i] = set([
                i 
                for i in route.get_attendance_type()
            ])
            
        return routes_by_type

    
    def limited_fleet_constr(self, model, routes_pool):
        y = [
            model.var_by_name("y_"+str(i))
            for i in range(len(routes_pool))
        ]

        routes_types_keys = [
            list(route.get_attendance_type())
            for route in routes_pool
        ]
        
        for i in range(len(routes_types_keys)):
            routes_types_keys[i].sort()
            routes_types_keys[i] = tuple(routes_types_keys[i])


        for fleet_type in self.fleet.values():
            fleet_type_key = list(fleet_type["types"])
            fleet_type_key.sort()
            fleet_type_key = tuple(fleet_type_key)
            routes_of_fleet_type = [
                y[i] 
                for i in range(len(routes_pool)) 
                if routes_types_keys[i] == fleet_type_key
            ]

            if (len(routes_of_fleet_type) == 0):
                continue

            count_fleet_type = sum(routes_of_fleet_type)

            c = model.add_constr(
                lin_expr=(count_fleet_type <= fleet_type["size"]),
                name="limited_fleet_"+str(fleet_type_key)
            )


    def route_was_chosen(self, model, routes_pool):
        y = [
            model.var_by_name("y_"+str(i))
            for i in range(len(routes_pool))
        ]

        z = [
            [
                model.var_by_name("z_"+str(i)+","+str(j)) 
                for j in self.fleet.keys()
            ]
            for i in range(len(routes_pool))
        ]
        # ERRADO AQUI TEM COMO NAO
        routes_by_type = self.get_routes_attended_by_vehicle_type(routes_pool)


        for i in range(len(routes_pool)):
            route_was_chosen = sum(
                z[i][att_type]
                for att_type in routes_by_type[i]
            )

            model.add_constr(
                lin_expr=(y[i] == route_was_chosen),
                name="y_"+str(i)+"_was_chosen"
            )

        

    def make_constraints(
        self, 
        model, 
        solution, 
        routes_with_request, 
        parameters
    ):
        routes_pool = parameters["routes_pool"]

        # Request cannot repeat
        self.request_chosen(
            model, 
            routes_pool,
            routes_with_request 
        )
        
        # Limited Fleet
        self.limited_fleet_constr(model, routes_pool)

        # Routes Cost cannot be worser than a maximum percentage
        # self.routes_max_cost_constr(model, solution, routes_pool)

        self.fixed_requests_must_be_in_solution_cosntr(model)

        # self.route_was_chosen(model, routes_pool)

        # for cons in model.constrs:
        #     print(cons)        

    

    def all_vehicles_in_solution(self, new_solution):
        total_fleet = 0
        for fleet_data in self.fleet.values():
            total_fleet += fleet_data["size"]

        if (new_solution.number_of_routes() < total_fleet):
            return False
        
        return True

    
    def complete_number_of_vehicles(self, new_solution):
        n = new_solution.copy()            

        for fleet_data in self.fleet.values():
            vehicles_of_type = 0
            
            for route in new_solution.routes():
                if (route.get_attendance_type() == fleet_data["types"]):
                    vehicles_of_type += 1
            number_vehicles_needed = fleet_data["size"] - vehicles_of_type
            while(number_vehicles_needed > 0):
                new_solution.add_route(Route(fleet_data["types"]))
                number_vehicles_needed -= 1
            
        # exit(0)

    def get_attr_relation_reader_heuristic(self):
        return {
            "vertices" : "vertices",
            "fleet" : "fleet",
            "fixed_routes_dict" : "fixed_routes_dict"
        }
