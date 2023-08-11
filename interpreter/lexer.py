from interpreter.token import Token, TokenTypes

class Lexer:
    SIMPLE_TOKEN_TYPES = {
        # This dictionary contains token types that:
        # 1) Consist of a single character only.
        # 2) And this character does not appear as the first character in any multi-character token type.
        TokenTypes.EOF.value: TokenTypes.EOF,
        TokenTypes.EOL.value: TokenTypes.EOL,
        TokenTypes.PLUS.value: TokenTypes.PLUS,
        TokenTypes.HYPHEN.value: TokenTypes.HYPHEN,
        TokenTypes.ASTERICK.value: TokenTypes.ASTERICK,
        TokenTypes.FORWARD_SLASH.value: TokenTypes.FORWARD_SLASH,
        TokenTypes.CARET.value: TokenTypes.CARET,
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
    
    def _peek_char(self):
        if (self._next_position == len(self._input)):
            return TokenTypes.EOF.value
        return self._get_char_at(self._next_position)
    
    def _is_whitespace(self):
        match(self._char):
            case ' ':
                return True
            case '\r':
                return True
            case '\t':
                return True
        return False
    
    def _skip_whitespace(self):
        while (self._is_whitespace()):
            self._next_char()
    
    def get_next_token(self) -> Token:
        self._next_char()
        self._skip_whitespace()
        
        simple_token_type: TokenTypes = self.SIMPLE_TOKEN_TYPES.get(self._char)
        if (simple_token_type):
            return Token(simple_token_type, simple_token_type.value)
        
        match(self._char):
            case TokenTypes.L_ANGLE_BRACKET.value:
                following_char = self._peek_char()
                match(following_char):
                    case TokenTypes.HYPHEN.value:
                        self._next_char()
                        return Token(TokenTypes.ASSIGNMENT, TokenTypes.ASSIGNMENT.value)
                    case TokenTypes.R_ANGLE_BRACKET.value:
                        self._next_char()
                        return Token(TokenTypes.NOT_EQUALS_TO, TokenTypes.NOT_EQUALS_TO.value)
                    case TokenTypes.EQUALS_TO.value:
                        self._next_char()
                        return Token(TokenTypes.LESSER_OR_EQUALS_TO, TokenTypes.LESSER_OR_EQUALS_TO.value)
                return Token(TokenTypes.L_ANGLE_BRACKET, TokenTypes.L_ANGLE_BRACKET.value)
            case TokenTypes.R_ANGLE_BRACKET.value:
                following_char = self._peek_char()
                match(following_char):
                    case TokenTypes.EQUALS_TO.value:
                        self._next_char()
                        return Token(TokenTypes.GREATER_OR_EQUALS_TO, TokenTypes.GREATER_OR_EQUALS_TO.value)
                return Token(TokenTypes.R_ANGLE_BRACKET, TokenTypes.R_ANGLE_BRACKET.value)
        
        return Token(TokenTypes.ILLEGAL, TokenTypes.ILLEGAL.value)