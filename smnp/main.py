import sys

from smnp.error.base import SmnpException
from smnp.program.interpreter import Interpreter


def main():
    try:

        Interpreter.interpretFile(sys.argv[1], printAst=True)

    except SmnpException as e:
        print(e.message())

    except KeyboardInterrupt:
        print("Program interrupted")
