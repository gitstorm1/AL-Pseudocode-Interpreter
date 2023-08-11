from interpreter.lexer import Lexer

input = """+-*/%&()"\'<-<<>
\t\r 
<=>>="""
lexer = Lexer(input)

token = lexer.get_next_token()
while (token.type.value != ''):
    print(token)
    token = lexer.get_next_token()
print(token)