import types


class NewEnum:
    @classmethod
    def get_names(cls):
        return [
            key
            for key in cls.__dict__.keys()
            if "__" not in key and not callable(getattr(cls, key))
        ]

    @classmethod
    def get_values(cls):
        return [
            getattr(cls, key)
            for key in cls.__dict__.keys()
            if "__" not in key and not callable(getattr(cls, key))
        ]

    @classmethod
    def get_functions(cls):
        functions = []
        for key in cls.__dict__.keys():
            if "__" not in key and isinstance(getattr(cls, key), types.FunctionType):
                functions.append(getattr(cls, key))
        return functions

        return [
            getattr(cls, key)
            for key in cls.__dict__.keys()
            if "__" not in key and callable(getattr(cls, key))
        ]

    @classmethod
    def get_classes(cls):
        classes = []
        for key in cls.__dict__.keys():
            if "__" not in key and isinstance(getattr(cls, key), type):
                classes.append(getattr(cls, key))
        return classes
