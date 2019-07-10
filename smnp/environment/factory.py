from smnp.environment.environment import Environment
from smnp.module import functions, methods


def createEnvironment():
    return Environment([{}], functions, methods)
 
