from src.solution_methods.basic_operators.RemovalOperatorDPDPTW \
    import RemovalOperatorDPDPTW


class RemovalOperatorDPDPTWNoCap(RemovalOperatorDPDPTW):
    def update_route_values(self, route, position, request):
        pickup_position, delivery_position = position
        
        for i in range(pickup_position, route.size()):
            arrival_time = (
                self.calculate_arrival_time(route, i)
            )

            route.arrival_times[i] = arrival_time