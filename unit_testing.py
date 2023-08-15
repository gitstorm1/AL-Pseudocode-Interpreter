# Local imports
from interpreter.parser.parser import Parser, Lexer

code = """DECLARE something : INTEGER
DECLARE haseeb : STRING
DECLARE zavi : DATE
DECLARE hey : 25.4
DECLARE another_thingoly : STRING"""

parser = Parser(Lexer(code))

parsed_program = parser.parse_program()

print("Code:")
print(code)

print("Parsed:")
for statement in parsed_program.statements:
    print(statement)

print("Errors:")
for error in parsed_program.errors:
    print(error)