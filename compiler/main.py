import sys

from compiler.Parser import Parser

if __name__ == "__main__":
    with open(sys.argv[1:][0], "r") as f:
        code = f.read()

    Parser.run(code)