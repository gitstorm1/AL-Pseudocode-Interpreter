from interpreter.token import Token, TokenTypes

class Lexer:
    SIMPLE_TOKEN_TYPES: dict[str, TokenTypes] = {
        # This dictionary contains token types that:
        # 1) Consist of a single character only.
        # 2) And this character does not appear as the first character in any multi-character token type.
        TokenTypes.EOF.value: TokenTypes.EOF,
        TokenTypes.EOL.value: TokenTypes.EOL,
        TokenTypes.PLUS.value: TokenTypes.PLUS,
        TokenTypes.HYPHEN.value: TokenTypes.HYPHEN,
        TokenTypes.ASTERISK.value: TokenTypes.ASTERISK,
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
        TokenTypes.COMMA.value: TokenTypes.COMMA,
    }
    
    KEYWORD_TOKEN_TYPES: dict[str, TokenTypes] = {
        TokenTypes.MODULUS.value: TokenTypes.MODULUS,
        TokenTypes.INT_DIV.value: TokenTypes.INT_DIV,
    }
    
    def __init__(self, input: str) -> None:
        self._input: str = input
        self._position: int = -1
        self._next_position: int = 0
        self._char: str = ''
    
    def _read_char(self, position: int) -> str:
        return self._input[position]
    
    def _advance(self) -> None:
        if (self._next_position == len(self._input)):
            self._char = TokenTypes.EOF.value
            return
        self._position = self._next_position
        self._next_position += 1
        self._char = self._read_char(self._position)
    
    def _peek_char(self) -> str:
        if (self._next_position == len(self._input)):
            return TokenTypes.EOF.value
        return self._read_char(self._next_position)
    
    def _is_whitespace(self) -> bool:
        match(self._char):
            case ' ':
                return True
            case '\r':
                return True
            case '\t':
                return True
        return False
    
    def _skip_whitespace(self) -> None:
        while (self._is_whitespace()):
            self._advance()
    
    def _is_alpha_or_underscore(self) -> bool:
        return ((self._char == '_') or (self._char.isalpha()))
    
    def _is_alphanumeric_or_underscore(self, char: str) -> bool:
        return ((char == '_') or (char.isalnum()))

    def _read_identifier(self) -> str:
        start_pos: int = self._position
        end_pos: int
        while (self._is_alphanumeric_or_underscore(self._peek_char())):
            self._advance()
            end_pos = self._position
        return self._input[(start_pos):(end_pos + 1)]
    
    def get_next_token(self) -> Token:
        self._advance()
        self._skip_whitespace()
        
        simple_token_type: TokenTypes = self.SIMPLE_TOKEN_TYPES.get(self._char)
        if (simple_token_type):
            return Token(simple_token_type, simple_token_type.value)
        
        match(self._char):
            case TokenTypes.FORWARD_SLASH.value:
                following_char: str = self._peek_char()
                match(following_char):
                    case TokenTypes.FORWARD_SLASH.value:
                        self._advance()
                        return Token(TokenTypes.SINGLE_LINE_COMMENT, TokenTypes.SINGLE_LINE_COMMENT.value)
                return Token(TokenTypes.FORWARD_SLASH, TokenTypes.FORWARD_SLASH.value)
            
            case TokenTypes.L_ANGLE_BRACKET.value:
                following_char: str = self._peek_char()
                match(following_char):
                    case TokenTypes.HYPHEN.value:
                        self._advance()
                        return Token(TokenTypes.ASSIGNMENT, TokenTypes.ASSIGNMENT.value)
                    
                    case TokenTypes.R_ANGLE_BRACKET.value:
                        self._advance()
                        return Token(TokenTypes.NOT_EQUALS_TO, TokenTypes.NOT_EQUALS_TO.value)
                    
                    case TokenTypes.EQUALS_TO.value:
                        self._advance()
                        return Token(TokenTypes.LESSER_OR_EQUALS_TO, TokenTypes.LESSER_OR_EQUALS_TO.value)
                    
                return Token(TokenTypes.L_ANGLE_BRACKET, TokenTypes.L_ANGLE_BRACKET.value)
            
            case TokenTypes.R_ANGLE_BRACKET.value:
                following_char: str = self._peek_char()
                match(following_char):
                    case TokenTypes.EQUALS_TO.value:
                        self._advance()
                        return Token(TokenTypes.GREATER_OR_EQUALS_TO, TokenTypes.GREATER_OR_EQUALS_TO.value)
                    
                return Token(TokenTypes.R_ANGLE_BRACKET, TokenTypes.R_ANGLE_BRACKET.value)
        
        if (self._is_alpha_or_underscore()):
            identifier: str = self._read_identifier()
            return Token(TokenTypes.IDENTIFIER, identifier)
        
        return Token(TokenTypes.ILLEGAL, TokenTypes.ILLEGAL.value)