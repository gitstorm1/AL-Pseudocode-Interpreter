# Local imports
from interpreter.parser.parser import Parser, Lexer
from interpreter.errors import PseudocodeError

code = """
hey <- "something"
anotherhey <- 'c'
fourth <- 2 * 2.5
fifth <- 5.5 >= (fourth AND hey[8]) <> anotherhey
fifth <- a = b
DECLARE test : INTEGER
CONSTANT a = FALSE
DECLARE hey : ARRAY[1:30+20-10, 1:50] OF REAL
hey[2, 4*2 MOD 5 / 2] <- 25.0
DECLARE copy : ARRAY[1:40, 1:50] OF REAL
copy <- hey
DECLARE _3d_array : ARRAY[1:100, 1:100, 1:100] OF REAL

OUTPUT "Abcd"
OUTPUT "Abcd", "Abcd", Abcd, other
OUTPUT "Join " & " strings " & " together."
OUTPUT anyexpression * b MOD 2
OUTPUT 'c'
OUTPUT "abc"
//OUTPUT

INPUT Abc
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