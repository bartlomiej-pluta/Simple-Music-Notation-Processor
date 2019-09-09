import argparse

VERSION = "0.1"
DESCRIPTION = """
    Simple Music Notation Processor is a command line tool enabling you to do some music stuff using custom domain-specific language.
"""

class CliParser(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(description=DESCRIPTION)
        self.parser.add_argument('file', nargs='*', help='a file containing SMNP code')
        self.parser.add_argument('-c', '--code', action='append', default=[], type=str, help='a string with SMNP code')
        self.parser.add_argument('-m', '--mic',  action='store_true', help='test microphone level')
        self.parser.add_argument('-C', '--config', type=argparse.FileType('-r'), help='a file containing settings (not implemented yet)')
        self.parser.add_argument('-p', '--params', action='append', help='pass arguments to program (not implemented yet)')
        self.parser.add_argument('-v', '--version', action='version')
        self.parser.add_argument('--tokens', action='store_true', help='print tokens of parsed code')
        self.parser.add_argument('--ast', action='store_true', help='print abstract syntax tree of parsed code')
        self.parser.add_argument('--dry-run', action='store_true', help='don\'t execute passed code')
        self.parser.version = VERSION

    def parse(self):
        return self.parser.parse_args()