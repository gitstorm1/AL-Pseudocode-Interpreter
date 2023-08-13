from interpreter.lexer import Lexer

input = """
-100.5+200.24--2.4
"""

lexer = Lexer(input)

token = lexer.get_next_token()
while (token.type.value != ''):
    print(token)
    token = lexer.get_next_token()
print(token)