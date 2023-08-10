from interpreter.token import Token, TokenTypes

class Lexer:
    def __init__(self, input: str):
        self._input = input
        self._position = 0
        self._next_position = 1
        self._char = self._get_char_at(self._position)
    
    def _get_char_at(self, position: int):
        return self._input[position]
    
    def _next_char(self):
        if (self._next_position == len(self._input)):
            self._char = ''
            return
        self._position = self._next_position
        self._next_position += 1
        self._char = self._get_char_at(self._position)
    
    def get_next_token(self) -> Token:
        token: Token
        match(self._char):
            case TokenTypes.PLUS.value:
                token = Token(TokenTypes.PLUS)
        
        return token