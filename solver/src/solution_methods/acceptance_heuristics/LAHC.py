from src.solution_methods.acceptance_heuristics.AcceptanceHeuristic import AcceptanceHeuristic




class LAHC(AcceptanceHeuristic):
    
    def __init__(self):
        super().__init__("Late Acceptance Hill Clibing")

    def initialize_class_attributes(self):
        super().initialize_class_attributes()
        self.obj_values_list = []
        self.list_size = None
        self.first_inserted_position = None


    def initialize_list_with_value(self, new_solution):
        for i in range(self.list_size):
            new_obj_value = (new_solution.cost(), new_solution.routes_cost())
            self.obj_values_list.append(new_obj_value)
            self.first_inserted_position = 0


    def accept(self, new_solution, obj_func, parameters=None):
        if(len(self.obj_values_list) == 0):
            self.initialize_list_with_value(new_solution)
            return True
        
        obj_value = self.obj_values_list[self.first_inserted_position]
        if (obj_func.solution_obj_better_than_value(new_solution, obj_value)):
            self.obj_values_list[self.first_inserted_position] = (
                new_solution.cost(),
                new_solution.routes_cost()
            )
            self.first_inserted_position = (
                (1 + self.first_inserted_position)
                % self.list_size
            )
            return True
        return False

    def get_attr_relation_reader(self):
        return super().get_attr_relation_reader()