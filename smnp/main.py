from smnp.calc import draft
from smnp.error.base import SmnpException


def main():
    try:
        #stdLibraryEnv = loadStandardLibrary()
        #Interpreter.interpretFile(sys.argv[1], printTokens=False, printAst=True, execute=False, baseEnvironment=stdLibraryEnv)
        draft()

    except SmnpException as e:
        print(e.message())

    except KeyboardInterrupt:
        print("Program interrupted")
