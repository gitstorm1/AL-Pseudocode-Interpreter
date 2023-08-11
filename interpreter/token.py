from enum import Enum

class TokenTypes(Enum):
    ILLEGAL = 'ILLEGAL'
    EOF = ''
    EOL = '\n'
    
    # Identifier (e.g. names of functions and variables)
    IDENTIFIER = 'IDENTIFIER'
    
    # Operators
    PLUS = '+'
    HYPHEN = '-'
    ASTERISK = '*'
    FORWARD_SLASH = '/'
    CARET = '^'
    MODULUS = 'MOD'
    INT_DIV = 'DIV'
    
    ASSIGNMENT = '<-'
    COLON = ':'
    
    # Comments
    SINGLE_LINE_COMMENT = '//'
    
    # Comparison
    EQUALS_TO = '='
    NOT_EQUALS_TO = '<>'
    AMPERSAND = '&'
    
    L_ANGLE_BRACKET = '<'
    LESSER_OR_EQUALS_TO = '<='
    
    R_ANGLE_BRACKET = '>'
    GREATER_OR_EQUALS_TO = '>='
    
    # Delimiters
    L_PARENTHESES = '('
    R_PARENTHESES = ')'
    
    L_SQ_BRACKET = '['
    R_SQ_BRACKET = ']'
    
    DOUBLE_QUOTE = '"'
    SINGLE_QUOTE = "'"
    
    COMMA = ','

class Token:
    def __init__(self, type: TokenTypes, literal: str):
        self.type = type
        self.literal = literal
    
    def __repr__(self) -> str:
        return f'Token({self.type}, {repr(self.literal)})'