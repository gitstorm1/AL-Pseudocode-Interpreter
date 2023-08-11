from interpreter.token import Token, TokenTypes

class Lexer:
    SIMPLE_TOKEN_TYPES = {
        # Token types of single (or less) characters that are not present in any multi-character token types.
        # e.g. the character of PLUS, '+', is not used in any composite token type, such as '++'.
        TokenTypes.EOF.value: TokenTypes.EOF,
        TokenTypes.PLUS.value: TokenTypes.PLUS,
        TokenTypes.HYPHEN.value: TokenTypes.HYPHEN,
        TokenTypes.ASTERICK.value: TokenTypes.ASTERICK,
        TokenTypes.FORWARD_SLASH.value: TokenTypes.FORWARD_SLASH,
        TokenTypes.CARET.value: TokenTypes.CARET,
        TokenTypes.PERCENT.value: TokenTypes.PERCENT,
        TokenTypes.COLON.value: TokenTypes.COLON,
        TokenTypes.EQUALS_TO.value: TokenTypes.EQUALS_TO,
        TokenTypes.AMPERSAND.value: TokenTypes.AMPERSAND,
        TokenTypes.L_PARENTHESES.value: TokenTypes.L_PARENTHESES,
        TokenTypes.R_PARENTHESES.value: TokenTypes.R_PARENTHESES,
        TokenTypes.L_SQ_BRACKET.value: TokenTypes.L_SQ_BRACKET,
        TokenTypes.R_SQ_BRACKET.value: TokenTypes.R_SQ_BRACKET,
        TokenTypes.DOUBLE_QUOTE.value: TokenTypes.DOUBLE_QUOTE,
        TokenTypes.SINGLE_QUOTE.value: TokenTypes.SINGLE_QUOTE,
        TokenTypes.COMMA.value: TokenTypes.PLUS,
    }
    
    def __init__(self, input: str):
        self._input = input
        self._position = -1
        self._next_position = 0
        self._char = ''
    
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
        self._next_char()
        
        simple_token_type: TokenTypes = self.SIMPLE_TOKEN_TYPES.get(self._char)
        if (simple_token_type):
            return Token(simple_token_type, simple_token_type.value)
        
        token: Token
        
        
        return token