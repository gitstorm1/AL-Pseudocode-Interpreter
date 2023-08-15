# Local imports
from interpreter.parser import Parser, Lexer

code = """
DECLARE something : INTEGER
DECLARE
DECLARE another_thing
"""

parser = Parser(Lexer(code))
parser.parse_program()