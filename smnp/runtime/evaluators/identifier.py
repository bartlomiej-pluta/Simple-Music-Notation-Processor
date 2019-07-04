from smnp.error.runtime import RuntimeException


def evaluateIdentifier(identifier, environment):
    try:
        value = environment.findVariable(identifier.identifier)
        return value
    except RuntimeException as e:
        e.pos = identifier.pos
        raise e