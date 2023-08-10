from enum import Enum

class TokenTypes(Enum):
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    CARET = '^'
    MODULUS = '%'
    
    AMPERSAND = '&'
    
    L_PARENTHESES = '('
    R_PARENTHESES = ')'
    
    DOUBLE_QUOTE = '"'
    SINGLE_QUOTE = "'"

class Token:
    def __init__(self, type: TokenTypes, literal: str):
        self.type = type
        self.literal = literal