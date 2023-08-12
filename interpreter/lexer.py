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
    
    def _is_alpha_or_underscore(self) -> bool:
        return ((self._char == '_') or (self._char.isalpha()))
    
    def _is_alphanumeric_or_underscore(self, char: str) -> bool:
        return ((char == '_') or (char.isalnum()))

    def _read_identifier(self) -> str:
        start_pos: int = self._position
        end_pos: int = start_pos
        while (self._is_alphanumeric_or_underscore(self._peek_char())):
            self._advance()
            end_pos = self._position
        return self._input[(start_pos):(end_pos + 1)]
    
    def _is_digit_or_period(self, char: str) -> bool:
        return ((char == TokenTypes.PERIOD.value) or (char.isdigit()))
    
    def _read_number(self) -> (int | float):
        start_pos: int = self._position
        end_pos: int = start_pos
        
        contains_period: bool = False
        
        while (self._is_digit_or_period(self._peek_char())):
            if (self._char == TokenTypes.PERIOD.value):
                if (contains_period):
                    raise Exception(f"A number cannot have more than one decimal point. line {self._line} column {self._column}")
                contains_period = True
            self._advance()
            end_pos = self._position
        
        if (self._read_char(end_pos) == '.'):
            raise Exception(f"A number cannot have the decimal point located at the end. line {self._line} column {self._column}")
        
        return (float if contains_period else int)(self._input[(start_pos):(end_pos + 1)])
    
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
                        self._advance()
                        return Token(TokenTypes.SINGLE_LINE_COMMENT, TokenTypes.SINGLE_LINE_COMMENT.value, line, column)
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
        
        if (self._is_alpha_or_underscore()):
            identifier: str = self._read_identifier()
            
            keyword_token_type: TokenTypes = self.KEYWORD_TOKEN_TYPES.get(identifier)
            if (keyword_token_type):
                return Token(keyword_token_type, identifier, line, column)
            
            return Token(TokenTypes.IDENTIFIER, identifier, line, column)
        
        if (self._is_digit_or_period(self._char)):
            number: (int | float) = self._read_number()
            
            if (type(number) == int):
                return Token(TokenTypes.INTEGER, str(number), line, column)
            
            return Token(TokenTypes.REAL, str(number), line, column)
        
        return Token(TokenTypes.ILLEGAL, TokenTypes.ILLEGAL.value, line, column)