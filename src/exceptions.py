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