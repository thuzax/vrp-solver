from os import stat
from src.GenericClass import GenericClass
from src import exceptions

class Route(GenericClass):
    instance = None
    
    route_cls = None
    reader_route_attr = None


    def __new__(cls, *args, **kwargs):
        if (len(cls.__subclasses__())):
            raise exceptions.ClassCannotBeInherited("Route")
        
        if (cls.instance is None):
            cls.instance = super(Route, cls).__new__(cls)
        
        route = cls.route_cls(*args, **kwargs)
        cls.instance.set_params(route)
        
        return route

    def __init__(self):
        if (not hasattr(self, "route_cls")):
            self.initialize_class_attributes()


    def set_params(self, route):
        if (self.reader_route_attr is None):
            return
        for param_name, param_value in self.reader_route_attr.items():
            route.set_attribute(param_name, param_value)


    @staticmethod
    def set_class(route_cls):
        Route.route_cls = route_cls
        Route.reader_route_attr = (
            Route.route_cls.get_attr_relation_reader_route()
        )

    def initialize_class_attributes(self):
        return super().initialize_class_attributes()

    @staticmethod
    def get_reader_route_attr_relation():
        return Route.reader_route_attr

    @staticmethod
    def update_route_class_params(params):
        Route.route_subclass_params = params
    
    
    @staticmethod
    def clear():
        for subcls in Route.__subclasses__():
            subcls.instance = None
            subcls.route_cls = None
            subcls.reader_route_attr = None
        Route.instance = None
        Route.route_cls = None
        Route.reader_route_attr = None