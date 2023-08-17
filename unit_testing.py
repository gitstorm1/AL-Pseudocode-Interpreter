# Local imports
from interpreter.parser.parser import Parser, Lexer

code = """
5+2+3 MOD 4 DIV 2 +4.4+hey*2/3
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