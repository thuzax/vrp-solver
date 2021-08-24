from src.ObjectsManager import ObjectsManager
from src import objective_functions

class ObjFunctionObjects(ObjectsManager):
    def add_object(self, obj):
        self.add_object_of_class(obj, objective_functions.ObjFunction)
