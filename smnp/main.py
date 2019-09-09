from smnp.cli.parser import CliParser
from smnp.error.base import SmnpException
from smnp.library.loader import loadStandardLibrary
from smnp.module.mic.lib.detector.noise import NoiseDetector
from smnp.program.interpreter import Interpreter


def interpretFile(args, file):
    stdLibraryEnv = loadStandardLibrary() if not args.dry_run else None
    Interpreter.interpretFile(file, printTokens=args.tokens, printAst=args.ast, execute=not args.dry_run, baseEnvironment=stdLibraryEnv)


def interpretString(args, string):
    stdLibraryEnv = loadStandardLibrary() if not args.dry_run else None
    Interpreter.interpretString(string, printTokens=args.tokens, printAst=args.ast, execute=not args.dry_run, baseEnvironment=stdLibraryEnv, source='<cli>')


def main():
    try:
        parser = CliParser()
        args = parser.parse()

        if args.mic:
            nd = NoiseDetector()
            nd.test()

        for code in args.code:
            interpretString(args, code)

        for file in args.file:
            interpretFile(args, file)

    except SmnpException as e:
        print(e.message())

    except KeyboardInterrupt:
        print("Program interrupted")

