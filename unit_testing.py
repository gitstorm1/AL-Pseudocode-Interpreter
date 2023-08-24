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

IF 5.2 THEN
    OUTPUT "Test"
    OUTPUT "Test"
ENDIF
"""
"""
IF (a * b) + 2 = 30 THEN
    OUTPUT "Yes"
    OUTPUT "Yes"
ELSE
    OUTPUT "ELSE"
    OUTPUT "ELSE"
ENDIF

IF (a * b) MOD 2 = 15 THEN
    OUTPUT "Yes1"
    OUTPUT "Yes1"
ELSEIF (a * b) + 2 = 30 THEN
    OUTPUT "ELSEIF"
    OUTPUT "ELSEIF"
ELSE
    IF TRUE THEN
        OUTPUT "ELSE"
    ENDIF
ENDIF

IF ChallengerScore > ChampionScore THEN
    IF ChallengerScore > HighestScore THEN
        OUTPUT ChallengerName, " is champion and highest scorer"
    ELSE
        OUTPUT ChallengerName, " is the new champion"
    ENDIF
ELSE
    OUTPUT ChampionName, " is still the champion"
    IF ChampionScore > HighestScore THEN
        OUTPUT ChampionName, " is also the highest scorer"
    ENDIF
ENDIF
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