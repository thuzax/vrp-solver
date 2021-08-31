class ObjectDoesNotHaveAttribute(Exception):
    def __init__(self, class_name, attribute_name):
        message = ""
        message += "Object from class " + str(class_name) + " "
        message += "does not have attribute " + str(attribute_name)

        super().__init__(message)

class ClassCannotBeInherited(Exception):
    def __init__(self, class_name):
        message = ""
        message += "Class " + class_name + " cannot be inherited."
        super().__init__(message)

class ObjectClassIsNotClassType(Exception):
    def __init__(self, obj_class_name, class_type_name):
        message = ""
        message += "Class " + obj_class_name + " is not a " 
        message += class_type_name + "."
        super().__init__(message)

class CouldNotRemoveWithShawRemoval(Exception):
    def __init__(self, request):
        message = ""
        message += "The request " + str(request) 
        message += "could not be removed with Shaw Removal Heuristic"
        return message

class WrongOrUndefinedStopCriteria(Exception):
    def __init__(self, heuristic_name):
        message = ""
        message += "The stop criteria for " + str(heuristic_name) 
        message += " is not an option or was undefined."
        return message