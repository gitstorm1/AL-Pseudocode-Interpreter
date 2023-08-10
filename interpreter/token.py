from enum import Enum

class TokenTypes(Enum):
    EOF = ''
    
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
    def __init__(self, type: TokenTypes, literal: str = None):
        self.type = type
        self.literal = (literal or type.value)