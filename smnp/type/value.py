class Value:
    def __init__(self, objectType, value):
        self.value = value

        if type(value) == objectType.value[0]:
            self.type = objectType
        else:
            raise RuntimeError(f"Invalid type '{objectType.name}' for value '{value}'")

    def stringify(self):
        return self.type.stringify(self.value)

    def __str__(self):
        return f"{self.type.name}({self.stringify()})"

    def __repr__(self):
        return self.__str__()
