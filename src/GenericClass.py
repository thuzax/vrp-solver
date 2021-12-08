from abc import ABC, ABCMeta, abstractmethod, abstractstaticmethod

from src import exceptions


class GenericClass(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    def set_attribute(self, name, value):
        if (not hasattr(self, name)):
            raise exceptions.ObjectDoesNotHaveAttribute(
                self.__class__.__name__, 
                name
            )
        self.__setattr__(name, value)


    def update_values(self, dict_update):
        for name, value in dict_update.items():
            self.set_attribute(name, value)


    @staticmethod
    def get_all_subclasses(cls):
        subclasses = []
        for subclass in cls.__subclasses__():
            subclasses.append(subclass)
            subclasses += GenericClass.get_all_subclasses(subclass)
        
        return subclasses

    @abstractmethod
    def initialize_class_attributes(self):
        pass
    
    
    @abstractstaticmethod
    def clear():
        pass