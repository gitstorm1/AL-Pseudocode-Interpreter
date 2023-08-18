# Local imports
from interpreter.parser.parser import Parser, Lexer

code = """
(3+2) + func(5, 20, (6*5/2)) * 2 MOD 5
"""

parser = Parser(Lexer(code))

parsed_program = parser.parse_program()

print("Code:")
print(code)

print("Parsed:")
for statement in parsed_program.statements:
    print(statement)

print("Errors:")
for error in parsed_program.errors:
    print(repr(error))