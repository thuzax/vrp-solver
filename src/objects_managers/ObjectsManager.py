from abc import abstractmethod
from src import exceptions
from src.GenericClass import GenericClass

class ObjectsManager:
    
    children_instances = {}

    def __new__(cls, *args, **kwargs):

        if (cls.__name__ not in cls.children_instances):
            cls_obj = super(ObjectsManager, cls).__new__(cls)
            cls.children_instances[cls.__name__] = cls_obj

        return cls.children_instances[cls.__name__]

    def __init__(self):
        super().__init__()
        if (not hasattr(self, "name")):
            self.name = self.__class__.__name__
            self.objs_list = []
            self.objs_dict = {}
    
    def add_object(self, obj, class_type):
        obj_class_name = obj.__class__.__name__
        if (isinstance(obj, class_type.__class__)):
            raise exceptions.ObjectClassIsNotClassType(
                obj_class_name,
                class_type.__name__
            )
        self.objs_list.append(obj)
        self.objs_dict[obj_class_name] = obj


    def get_by_name(self, class_name):
        return self.objs_dict[class_name]


    def get_list(self):
        return self.objs_list


    @staticmethod
    def clear():
        ObjectsManager.children_instances.clear()