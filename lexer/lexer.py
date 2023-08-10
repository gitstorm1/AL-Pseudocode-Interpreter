class Lexer:
    def __init__(self, input: str):
        self._input = input
        self._position = 0
        self._next_position = 1
        self._char = self._get_char_at(self._position)
    
    def _get_char_at(self, position: int):
        return self._input[position]
    
    def get_next_token():
        pass

if (__name__ == '__main__'):
    input = '+-*/%&()"\''
    lexer = Lexer(input)
    print(lexer._char)