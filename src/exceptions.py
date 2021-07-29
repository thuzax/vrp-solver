class ObjectDoesNotHaveAttribute(Exception):
    def __init__(self, class_name, attribute_name):
        message = ""
        message += "Object from class " + str(class_name) + " "
        message += "does not have attribute " + str(attribute_name)

        super().__init__(message)