# Local imports
from interpreter.parser.parser import Parser, Lexer

code = """
(3+2) AND -NOT test.member(5, 2.0, (6*5/2)) * 2 + h(1,2,0,5) - array[2, 4*3 MOD 2] + object.member.array[a] + object.member.array() & "abc" & "another"
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