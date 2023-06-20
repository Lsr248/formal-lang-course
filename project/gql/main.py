import sys

from project.gql.Visitor import Visitor
from project.gql.exceptions import *
from project.gql.parser import get_parser, accept


def read_script(filepath):
    """Read script from file with .flp extension."""
    if not filepath.name.endswith(".flp"):
        raise IncorrectExtensionException()
    try:
        file = filepath.open()
    except FileNotFoundError as e:
        raise IncorrectPathException(filepath.name) from e
    return "".join(file.readlines())


if __name__ == "__main__":
    program = read_script(sys.argv[1])
    if not accept(program):
        raise IncorrectSyntaxError()
    try:
        tree = get_parser(program).prog()
        visitor = Visitor()
        visitor.visit(tree)
    except SomethingException as e:
        sys.stdout.write(f"Exception: {e.msg}\n")
        exit(1)
    exit(0)
