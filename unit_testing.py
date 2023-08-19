# Local imports
from interpreter.parser.parser import Parser, Lexer
from interpreter.errors import PseudocodeError

code = """
hey <- "something"
anotherhey <- 'c'
fourth <- 2 * 2.5
fifth <- 5.5 >= (fourth AND hey[8]) <> anotherhey
fifth <- a = b
"""

print("********************")
print("::CODE::")
print("********")
print(code)
print("********************")

parser = Parser(Lexer(code))

try:
    parsed_program = parser.parse_program()
except PseudocodeError as err:
    print(err)
else:
    print("********************")
    print("::PARSED::")
    print("**********")
    for statement in parsed_program.statements:
        print(statement)
    print("********************")