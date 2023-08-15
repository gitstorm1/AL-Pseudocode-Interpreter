# Local imports
from interpreter.parser import Parser, Lexer

code = """
DECLARE something : INTEGER
DECLARE haseeb : STRING
DECLARE zavi : DATE
DECLARE hey : 25.4
DECLARE another_thingoly : STRING
"""

parser = Parser(Lexer(code))

program = parser.parse_program()

print("* AFTER PARSE:")
for statement in program.statements:
    print(statement)