from interpreter.lexer import Lexer

input = '+-*/%&()"\''
lexer = Lexer(input)
print(lexer.get_next_token())