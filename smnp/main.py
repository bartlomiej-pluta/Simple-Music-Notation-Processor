import sys

from smnp.error.base import SmnpException
from smnp.program.interpreter import Interpreter


def main():
    try:
        #stdLibraryEnv = loadStandardLibrary()
        Interpreter.interpretFile(sys.argv[1], printTokens=False, printAst=True, baseEnvironment=None)

    except SmnpException as e:
        print(e.message())

    except KeyboardInterrupt:
        print("Program interrupted")
