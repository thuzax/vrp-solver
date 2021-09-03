import inspect

import src


def create_class_by_name(class_name, class_data):
    class_type = getattr(
        src, 
        class_name
    )
    class_object = class_type()

    for attribute, value in class_data.items():
        if (getattr(class_object, attribute) is None):
            class_object.set_attribute(attribute, value)

    return class_object