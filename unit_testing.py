# Local imports
from interpreter.parser.parser import Parser, Lexer

code = """
a+b
hey <- "something"
anotherhey <- 'c'
fourth <- 2 * 2.5
fifth <- 5.5 >= (fourth AND hey[8]) <> anotherhey
fifth = 2
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