class Value:
    def __init__(self, objectType, value, properties=None):
        if properties is None:
            properties = {}

        self.value = value
        self.properties = properties

        if objectType.value[0] is None or type(value) == objectType.value[0]:
            self.type = objectType

        elif type(value) == Value:
            raise RuntimeError("Trying to pass object of 'Value' type as value of it")

        else:
            raise RuntimeError(f"Invalid type '{objectType.name}' for value '{value}'")

    def stringify(self):
        return self.type.stringify(self.value)

    def decompose(self):
        from smnp.type.model import Type
        if self.type != Type.LIST:
            raise RuntimeError(f"Method 'decompose' can be applied only for lists")

        if len(self.value) == 1:
            return Value(self.value[0].type, self.value[0].value)

        return self

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return hash(self.type) ^ hash(self.value)

    def __str__(self):
        return f"{self.type.name}({self.value})"

    def __repr__(self):
        return self.__str__()
