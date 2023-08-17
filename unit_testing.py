# Local imports
from interpreter.parser.parser import Parser, Lexer

code = """
(-5 + 2)*3 /hey MOD 40 DIV 95.5 >= (((5 + 2))) AND humans.haseeb.brain.size^2^2^2 = 0 AND zavi.(((brain.iq))) = 0
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