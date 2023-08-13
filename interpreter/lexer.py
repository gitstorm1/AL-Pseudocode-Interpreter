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
        TokenTypes.INTEGER.value: TokenTypes.INTEGER,
        TokenTypes.REAL.value: TokenTypes.REAL,
        TokenTypes.CHAR.value: TokenTypes.CHAR,
        TokenTypes.STRING.value: TokenTypes.STRING,
        TokenTypes.BOOLEAN.value: TokenTypes.BOOLEAN,
        TokenTypes.DATE.value: TokenTypes.DATE,
        
        TokenTypes.WHILE.value: TokenTypes.WHILE,
        TokenTypes.ENDWHILE.value: TokenTypes.ENDWHILE,
        
        TokenTypes.REPEAT.value: TokenTypes.REPEAT,
        TokenTypes.UNTIL.value: TokenTypes.UNTIL,
        
        TokenTypes.FOR.value: TokenTypes.FOR,
        TokenTypes.TO.value: TokenTypes.TO,
        TokenTypes.STEP.value: TokenTypes.STEP,
        TokenTypes.NEXT.value: TokenTypes.NEXT,
        
        TokenTypes.DECLARE.value: TokenTypes.DECLARE,
        TokenTypes.CONSTANT.value: TokenTypes.CONSTANT,
        
        TokenTypes.ARRAY.value: TokenTypes.ARRAY,
        TokenTypes.OF.value: TokenTypes.OF,
        
        TokenTypes.TYPE.value: TokenTypes.TYPE,
        TokenTypes.ENDTYPE.value: TokenTypes.ENDTYPE,
        
        TokenTypes.INPUT.value: TokenTypes.INPUT,
        TokenTypes.OUTPUT.value: TokenTypes.OUTPUT,
        
        TokenTypes.AND.value: TokenTypes.AND,
        TokenTypes.OR.value: TokenTypes.OR,
        TokenTypes.NOT.value: TokenTypes.NOT,
        
        TokenTypes.PROCEDURE.value: TokenTypes.PROCEDURE,
        TokenTypes.ENDPROCEDURE.value: TokenTypes.ENDPROCEDURE,
        TokenTypes.CALL.value: TokenTypes.CALL,
        
        TokenTypes.BYREF.value: TokenTypes.BYREF,
        
        TokenTypes.FUNCTION.value: TokenTypes.FUNCTION,
        TokenTypes.RETURNS.value: TokenTypes.RETURNS,
        TokenTypes.RETURN.value: TokenTypes.RETURN,
        TokenTypes.ENDFUNCTION.value: TokenTypes.ENDFUNCTION,
        
        TokenTypes.IF.value: TokenTypes.IF,
        TokenTypes.THEN.value: TokenTypes.THEN,
        TokenTypes.ELSEIF.value: TokenTypes.ELSEIF,
        TokenTypes.ENDIF.value: TokenTypes.ENDIF,
        
        TokenTypes.CASE.value: TokenTypes.CASE,
        TokenTypes.OTHERWISE.value: TokenTypes.OTHERWISE,
        TokenTypes.ENDCASE.value: TokenTypes.ENDCASE,
        
        TokenTypes.MODULUS.value: TokenTypes.MODULUS,
        TokenTypes.INT_DIV.value: TokenTypes.INT_DIV,
        
        TokenTypes.OPENFILE.value: TokenTypes.OPENFILE,
        TokenTypes.READFILE.value: TokenTypes.READFILE,
        TokenTypes.WRITEFILE.value: TokenTypes.WRITEFILE,
        TokenTypes.READ.value: TokenTypes.READ,
        TokenTypes.WRITE.value: TokenTypes.WRITE,
        TokenTypes.APPEND.value: TokenTypes.APPEND,
        
        TokenTypes.PUBLIC.value: TokenTypes.PUBLIC,
        TokenTypes.PRIVATE.value: TokenTypes.PRIVATE,
        TokenTypes.CLASS.value: TokenTypes.CLASS,
        TokenTypes.ENDCLASS.value: TokenTypes.ENDCLASS,
        TokenTypes.INHERITS.value: TokenTypes.INHERITS,
        TokenTypes.NEW.value: TokenTypes.NEW,
    }
    
    def __init__(self, input: str) -> None:
        self._input: str = input
        
        self._position: int = -1
        self._next_position: int = 0
        
        self._line: int = 1
        self._column: int = (self._position + 1)
        
        self._char: str = ''
    
    def _read_char(self, position: int) -> str:
        return self._input[position]
    
    def _advance(self) -> None:
        self._position = self._next_position
        self._next_position += 1
        self._column += 1
        self._char = TokenTypes.EOF.value if (self._position == len(self._input)) else self._read_char(self._position)
    
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
    
    def _skip_comment(self) -> None:
        while (TokenTypes.EOL.value != self._peek_char() != TokenTypes.EOF.value):
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
    
    def _read_number(self) -> tuple[str, TokenTypes]:
        start_pos: int = self._position
        end_pos: int = start_pos
        
        number_token_type: TokenTypes = TokenTypes.REAL if (self._read_char(start_pos) == TokenTypes.PERIOD.value) else TokenTypes.INTEGER
        
        while True:
            following_char: str = self._peek_char()
            if (not following_char.isdigit()):
                if (following_char == TokenTypes.PERIOD.value):
                    if (number_token_type != TokenTypes.REAL):
                        number_token_type = TokenTypes.REAL
                    else:
                        raise Exception(f"A number cannot have more than one decimal point.\n[Line = {self._line}, Column = {self._column}]")
                else:
                    break
            self._advance()
            end_pos = self._position
        
        return (self._input[start_pos : (end_pos + 1)], number_token_type)
    
    def get_next_token(self) -> Token:
        self._advance()
        self._skip_whitespace()
        
        line: int = self._line
        column: int = self._column
        
        simple_token_type: TokenTypes = self.SIMPLE_TOKEN_TYPES.get(self._char)
        if (simple_token_type):
            if (simple_token_type == TokenTypes.EOL):
                self._line += 1
                self._column = 0
            return Token(simple_token_type, simple_token_type.value, line, column)
        
        match(self._char):
            case TokenTypes.FORWARD_SLASH.value:
                following_char: str = self._peek_char()
                match(following_char):
                    case TokenTypes.FORWARD_SLASH.value:
                        self._skip_comment()
                        return self.get_next_token()
                return Token(TokenTypes.FORWARD_SLASH, TokenTypes.FORWARD_SLASH.value, line, column)
            
            case TokenTypes.L_ANGLE_BRACKET.value:
                following_char: str = self._peek_char()
                match(following_char):
                    case TokenTypes.HYPHEN.value:
                        self._advance()
                        return Token(TokenTypes.ASSIGNMENT, TokenTypes.ASSIGNMENT.value, line, column)
                    
                    case TokenTypes.R_ANGLE_BRACKET.value:
                        self._advance()
                        return Token(TokenTypes.NOT_EQUALS_TO, TokenTypes.NOT_EQUALS_TO.value, line, column)
                    
                    case TokenTypes.EQUALS_TO.value:
                        self._advance()
                        return Token(TokenTypes.LESSER_OR_EQUALS_TO, TokenTypes.LESSER_OR_EQUALS_TO.value, line, column)
                    
                return Token(TokenTypes.L_ANGLE_BRACKET, TokenTypes.L_ANGLE_BRACKET.value, line, column)
            
            case TokenTypes.R_ANGLE_BRACKET.value:
                following_char: str = self._peek_char()
                match(following_char):
                    case TokenTypes.EQUALS_TO.value:
                        self._advance()
                        return Token(TokenTypes.GREATER_OR_EQUALS_TO, TokenTypes.GREATER_OR_EQUALS_TO.value, line, column)
                    
                return Token(TokenTypes.R_ANGLE_BRACKET, TokenTypes.R_ANGLE_BRACKET.value, line, column)

            case TokenTypes.PERIOD.value:
                following_char: str = self._peek_char()
                if (not following_char.isdigit()):
                    return Token(TokenTypes.PERIOD, TokenTypes.PERIOD.value, line, column)
        
        if ((self._char.isalpha()) or (self._char == '_')):
            identifier: str = self._read_identifier()
            
            token_type: TokenTypes = (self.KEYWORD_TOKEN_TYPES.get(identifier) or TokenTypes.IDENTIFIER)
            
            return Token(token_type, identifier, line, column)
        
        if ((self._char.isdigit()) or (self._char == TokenTypes.PERIOD.value)):
            number, number_token_type = self._read_number()
            
            return Token(number_token_type, number, line, column)
        
        return Token(TokenTypes.ILLEGAL, TokenTypes.ILLEGAL.value, line, column)