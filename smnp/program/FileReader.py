def readLines(file):
    with open(file, 'r') as source:
        return [line.rstrip('\n') for line in source.readlines()]