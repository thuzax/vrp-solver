from src import constraints
from src.ObjectsManager import ObjectsManager

class ConstraintsObjects(ObjectsManager):
    def add_object(self, obj):
        self.add_object_of_class(obj, constraints.Constraint)