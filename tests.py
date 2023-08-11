from interpreter.lexer import Lexer

input = """

\r\t
+ - * / ^ <- : // = <> & < <= > >= () [] " ' , MOD DIV

"""
lexer = Lexer(input)

token = lexer.get_next_token()
while (token.type.value != ''):
    print(token)
    token = lexer.get_next_token()
print(token)

print("a" < "A")