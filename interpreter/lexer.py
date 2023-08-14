# Local imports
from .token import Token, TokenType

class Lexer:
    SIMPLE_TOKEN_TYPES: dict[str, TokenType] = {
        # This dictionary contains token types that:
        # 1) Consist of a single character only.
        # 2) And this character does not appear as the first character in any multi-character token type.
        TokenType.EOF.value: TokenType.EOF,
        TokenType.EOL.value: TokenType.EOL,
        TokenType.PLUS.value: TokenType.PLUS,
        TokenType.HYPHEN.value: TokenType.HYPHEN,
        TokenType.ASTERISK.value: TokenType.ASTERISK,
        TokenType.CARET.value: TokenType.CARET,
        TokenType.COLON.value: TokenType.COLON,
        TokenType.EQUALS_TO.value: TokenType.EQUALS_TO,
        TokenType.AMPERSAND.value: TokenType.AMPERSAND,
        TokenType.L_PARENTHESES.value: TokenType.L_PARENTHESES,
        TokenType.R_PARENTHESES.value: TokenType.R_PARENTHESES,
        TokenType.L_SQ_BRACKET.value: TokenType.L_SQ_BRACKET,
        TokenType.R_SQ_BRACKET.value: TokenType.R_SQ_BRACKET,
        TokenType.COMMA.value: TokenType.COMMA,
    }
    
    KEYWORD_TOKEN_TYPES: dict[str, TokenType] = {
        TokenType.INTEGER.value: TokenType.INTEGER,
        TokenType.REAL.value: TokenType.REAL,
        TokenType.CHAR.value: TokenType.CHAR,
        TokenType.STRING.value: TokenType.STRING,
        TokenType.BOOLEAN.value: TokenType.BOOLEAN,
        TokenType.DATE.value: TokenType.DATE,
        
        TokenType.WHILE.value: TokenType.WHILE,
        TokenType.ENDWHILE.value: TokenType.ENDWHILE,
        
        TokenType.REPEAT.value: TokenType.REPEAT,
        TokenType.UNTIL.value: TokenType.UNTIL,
        
        TokenType.FOR.value: TokenType.FOR,
        TokenType.TO.value: TokenType.TO,
        TokenType.STEP.value: TokenType.STEP,
        TokenType.NEXT.value: TokenType.NEXT,
        
        TokenType.DECLARE.value: TokenType.DECLARE,
        TokenType.CONSTANT.value: TokenType.CONSTANT,
        
        TokenType.ARRAY.value: TokenType.ARRAY,
        TokenType.OF.value: TokenType.OF,
        
        TokenType.TYPE.value: TokenType.TYPE,
        TokenType.ENDTYPE.value: TokenType.ENDTYPE,
        
        TokenType.INPUT.value: TokenType.INPUT,
        TokenType.OUTPUT.value: TokenType.OUTPUT,
        
        TokenType.AND.value: TokenType.AND,
        TokenType.OR.value: TokenType.OR,
        TokenType.NOT.value: TokenType.NOT,
        
        TokenType.PROCEDURE.value: TokenType.PROCEDURE,
        TokenType.ENDPROCEDURE.value: TokenType.ENDPROCEDURE,
        TokenType.CALL.value: TokenType.CALL,
        
        TokenType.BYREF.value: TokenType.BYREF,
        
        TokenType.FUNCTION.value: TokenType.FUNCTION,
        TokenType.RETURNS.value: TokenType.RETURNS,
        TokenType.RETURN.value: TokenType.RETURN,
        TokenType.ENDFUNCTION.value: TokenType.ENDFUNCTION,
        
        TokenType.IF.value: TokenType.IF,
        TokenType.THEN.value: TokenType.THEN,
        TokenType.ELSEIF.value: TokenType.ELSEIF,
        TokenType.ENDIF.value: TokenType.ENDIF,
        
        TokenType.CASE.value: TokenType.CASE,
        TokenType.OTHERWISE.value: TokenType.OTHERWISE,
        TokenType.ENDCASE.value: TokenType.ENDCASE,
        
        TokenType.MODULUS.value: TokenType.MODULUS,
        TokenType.INT_DIV.value: TokenType.INT_DIV,
        
        TokenType.OPENFILE.value: TokenType.OPENFILE,
        TokenType.READFILE.value: TokenType.READFILE,
        TokenType.WRITEFILE.value: TokenType.WRITEFILE,
        TokenType.READ.value: TokenType.READ,
        TokenType.WRITE.value: TokenType.WRITE,
        TokenType.APPEND.value: TokenType.APPEND,
        
        TokenType.PUBLIC.value: TokenType.PUBLIC,
        TokenType.PRIVATE.value: TokenType.PRIVATE,
        TokenType.CLASS.value: TokenType.CLASS,
        TokenType.ENDCLASS.value: TokenType.ENDCLASS,
        TokenType.INHERITS.value: TokenType.INHERITS,
        TokenType.NEW.value: TokenType.NEW,
    }
    
    def __init__(self, input: str) -> None:
        self._input: str = input
        
        self._position: int = -1
        self._char: str = TokenType.EOF.value
        
        self._line: int = 1
        self._column: int = (self._position + 1)
    
    def _advance(self, distance: int = 1) -> None:
        self._position += distance
        self._column += distance
        self._char = TokenType.EOF.value if (self._position >= len(self._input)) else self._input[self._position]
    
    def _peek_char(self, distance: int = 1) -> str:
        peek_position: int = (self._position + distance)
        if (peek_position >= len(self._input)):
            return TokenType.EOF.value
        return self._input[peek_position]
    
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
    
    def _skip_comment(self) -> None:
        while (TokenType.EOL.value != self._peek_char() != TokenType.EOF.value):
            self._advance()
    
    def _is_alphanumeric_or_underscore(self, char: str) -> bool:
        return ((char.isalnum()) or (char == '_'))

    def _read_identifier(self) -> str:
        start_pos: int = self._position
        end_pos: int = start_pos
        while (self._is_alphanumeric_or_underscore(self._peek_char())):
            self._advance()
            end_pos = self._position
        return self._input[start_pos : (end_pos + 1)]
    
    def _read_number(self) -> tuple[str, TokenType]:
        start_pos: int = self._position
        end_pos: int = start_pos
        
        number_token_type: TokenType = TokenType.REAL if (self._input[start_pos] == TokenType.PERIOD.value) else TokenType.INTEGER
        
        while True:
            following_char: str = self._peek_char()
            if (not following_char.isdigit()):
                if (following_char == TokenType.PERIOD.value):
                    if (number_token_type != TokenType.REAL):
                        number_token_type = TokenType.REAL
                    else:
                        raise Exception(f"A number cannot have more than one decimal point.\n[Line = {self._line}, Column = {self._column}]")
                else:
                    break
            self._advance()
            end_pos = self._position
        
        return (self._input[start_pos : (end_pos + 1)], number_token_type)
    
    def _read_char(self) -> str:
        if (self._peek_char() == TokenType.SINGLE_QUOTE.value):
            self._advance()
            return ''
        elif (self._peek_char(2) == TokenType.SINGLE_QUOTE.value):
            char: str = self._input[(self._position + 1)]
            self._advance(2)
            return char
        
        raise Exception(f"Single quotes must be in pairs and can only contain a single character.\n[Line = {self._line}, Column = {self._column}]")
    
    def _read_string(self) -> str:
        start_pos: int = self._position
        end_pos: int
        while (TokenType.EOL.value != self._peek_char() != TokenType.EOF.value):
            self._advance()
            end_pos = self._position
            
            if (self._char == TokenType.DOUBLE_QUOTE.value):
                break
        else:
            raise Exception(f"Double quotes must be in pairs and strings cannot stretch across multiple lines.\n[Line = {self._line}, Column = {self._column}]")
        
        return self._input[(start_pos + 1) : end_pos]
    
    def get_next_token(self) -> Token:
        self._advance()
        self._skip_whitespace()
        
        line: int = self._line
        column: int = self._column
        
        simple_token_type: TokenType = self.SIMPLE_TOKEN_TYPES.get(self._char)
        if (simple_token_type):
            if (simple_token_type == TokenType.EOL):
                self._line += 1
                self._column = 0
            return Token(simple_token_type, simple_token_type.value, line, column)
        
        match(self._char):
            case TokenType.FORWARD_SLASH.value:
                following_char: str = self._peek_char()
                match(following_char):
                    case TokenType.FORWARD_SLASH.value:
                        self._skip_comment()
                        return self.get_next_token()
                return Token(TokenType.FORWARD_SLASH, TokenType.FORWARD_SLASH.value, line, column)
            
            case TokenType.L_ANGLE_BRACKET.value:
                following_char: str = self._peek_char()
                match(following_char):
                    case TokenType.HYPHEN.value:
                        self._advance()
                        return Token(TokenType.ASSIGNMENT, TokenType.ASSIGNMENT.value, line, column)
                    
                    case TokenType.R_ANGLE_BRACKET.value:
                        self._advance()
                        return Token(TokenType.NOT_EQUALS_TO, TokenType.NOT_EQUALS_TO.value, line, column)
                    
                    case TokenType.EQUALS_TO.value:
                        self._advance()
                        return Token(TokenType.LESSER_OR_EQUALS_TO, TokenType.LESSER_OR_EQUALS_TO.value, line, column)
                    
                return Token(TokenType.L_ANGLE_BRACKET, TokenType.L_ANGLE_BRACKET.value, line, column)
            
            case TokenType.R_ANGLE_BRACKET.value:
                following_char: str = self._peek_char()
                match(following_char):
                    case TokenType.EQUALS_TO.value:
                        self._advance()
                        return Token(TokenType.GREATER_OR_EQUALS_TO, TokenType.GREATER_OR_EQUALS_TO.value, line, column)
                    
                return Token(TokenType.R_ANGLE_BRACKET, TokenType.R_ANGLE_BRACKET.value, line, column)

            case TokenType.SINGLE_QUOTE.value:
                token: Token = Token(TokenType.CHAR, self._read_char(), line, column)
                token.is_literal = True
                return token
            
            case TokenType.DOUBLE_QUOTE.value:
                token: Token = Token(TokenType.STRING, self._read_string(), line, column)
                token.is_literal = True
                return token
            
            case TokenType.PERIOD.value:
                following_char: str = self._peek_char()
                if (not following_char.isdigit()):
                    return Token(TokenType.PERIOD, TokenType.PERIOD.value, line, column)
        
        if ((self._char.isalpha()) or (self._char == '_')):
            identifier: str = self._read_identifier()
            
            token_type: TokenType = (self.KEYWORD_TOKEN_TYPES.get(identifier) or TokenType.IDENTIFIER)
            
            return Token(token_type, identifier, line, column)
        
        if ((self._char.isdigit()) or (self._char == TokenType.PERIOD.value)):
            number, number_token_type = self._read_number()
            
            token: Token = Token(number_token_type, number, line, column)
            token.is_literal = True
            
            return token
        
        return Token(TokenType.ILLEGAL, self._char, line, column)