from interpreter.lexer import Lexer

input = """line1column1 line1column14
line2column1 line2column14 12355-. BYREF FUNCTION ENDFUNCTION PROCEDURE lolbruh
// test
line4column1 .12 .1 5 65 // lol"""

lexer = Lexer(input)

token = lexer.get_next_token()
while (token.type.value != ''):
    print(token)
    token = lexer.get_next_token()
print(token)