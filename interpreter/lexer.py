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
            self._char = TokenTypes.EOF.value
            return
        self._position = self._next_position
        self._next_position += 1
        self._char = self._get_char_at(self._position)
    
    def get_next_token(self) -> Token:
        token: Token
        
        match(self._char):
            case TokenTypes.PLUS.value:
                token = Token(TokenTypes.PLUS)
            case TokenTypes.MINUS.value:
                token = Token(TokenTypes.MINUS)
            case TokenTypes.MULTIPLY.value:
                token = Token(TokenTypes.MULTIPLY)
            case TokenTypes.DIVIDE.value:
                token = Token(TokenTypes.DIVIDE)
            case TokenTypes.CARET.value:
                token = Token(TokenTypes.CARET)
            case TokenTypes.MODULUS.value:
                token = Token(TokenTypes.MODULUS)
            case TokenTypes.AMPERSAND.value:
                token = Token(TokenTypes.AMPERSAND)
            case TokenTypes.L_PARENTHESES.value:
                token = Token(TokenTypes.L_PARENTHESES)
            case TokenTypes.R_PARENTHESES.value:
                token = Token(TokenTypes.R_PARENTHESES)
            case TokenTypes.DOUBLE_QUOTE.value:
                token = Token(TokenTypes.DOUBLE_QUOTE)
            case TokenTypes.SINGLE_QUOTE.value:
                token = Token(TokenTypes.SINGLE_QUOTE)
            case TokenTypes.EOF.value:
                token = Token(TokenTypes.EOF)
        
        self._next_char()
        return token