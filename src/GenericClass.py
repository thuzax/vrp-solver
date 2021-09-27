from abc import ABC, ABCMeta, abstractmethod

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

    @abstractmethod
    def initialize_class_attributes(self):
        pass