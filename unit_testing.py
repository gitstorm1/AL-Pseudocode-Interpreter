# Local imports
from interpreter.parser.parser import Parser, Lexer

code = """DECLARE something : STRING
something <- "Truly something" """

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