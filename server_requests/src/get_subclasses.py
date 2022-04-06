def get_all_subclasses(cls):
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses += get_all_subclasses(subclass)

    return subclasses