from enum import Enum

class TokenTypes(Enum):
    ##### Special tokens
    ILLEGAL = 'ILLEGAL'
    EOF = ''
    EOL = '\n'
    
    ##### For function and variable names
    IDENTIFIER = 'IDENTIFIER'
    
    ##### Native datatypes
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    CHAR = 'CHAR'
    STRING = 'STRING'
    BOOLEAN = 'BOOLEAN'
    DATE = 'DATE'
    
    ##### Keywords
    # WHILE loop
    WHILE = 'WHILE'
    ENDWHILE = 'ENDWHILE'
    
    # REPEAT UNTIL loop
    REPEAT = 'REPEAT'
    UNTIL = 'UNTIL'
    
    # FOR loop
    FOR = 'FOR'
    TO = 'TO'
    STEP = 'STEP'
    NEXT = 'NEXT'
    
    # Declaring of variables and constants
    DECLARE = 'DECLARE'
    CONSTANT = 'CONSTANT'
    
    # Declaring of arrays
    ARRAY = 'ARRAY'
    OF = 'OF'
    
    # Declaring of user-defined types, including pointers
    TYPE = 'TYPE'
    ENDTYPE = 'ENDTYPE'
    
    # Console input and output
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'
    
    # Logical operators
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    
    # Procedure definition and calling
    PROCEDURE = 'PROCEDURE'
    ENDPROCEDURE = 'ENDPROCEDURE'
    CALL = 'CALL'
    
    # Making a parameter pass by reference in a procedure
    BYREF = 'BYREF'
    
    # Function definition and returning
    FUNCTION = 'FUNCTION'
    RETURNS = 'RETURNS'
    RETURN = 'RETURN'
    ENDFUNCTION = 'ENDFUNCTION'
    
    # Selection keywords
    IF = 'IF'
    THEN = 'THEN'
    ELSEIF = 'ELSEIF'
    ENDIF = 'ENDIF'
    
    CASE = 'CASE'
    OTHERWISE = 'OTHERWISE'
    ENDCASE = 'ENDCASE'
    
    ##### Operators
    MODULUS = 'MOD'
    INT_DIV = 'DIV'
    
    PLUS = '+'
    HYPHEN = '-'
    ASTERISK = '*'
    FORWARD_SLASH = '/'
    CARET = '^'
    PERIOD = '.'
    
    ASSIGNMENT = '<-'
    COLON = ':'
    
    ##### Comparison
    EQUALS_TO = '='
    NOT_EQUALS_TO = '<>'
    AMPERSAND = '&'
    
    L_ANGLE_BRACKET = '<'
    LESSER_OR_EQUALS_TO = '<='
    
    R_ANGLE_BRACKET = '>'
    GREATER_OR_EQUALS_TO = '>='
    
    ##### Delimiters
    L_PARENTHESES = '('
    R_PARENTHESES = ')'
    
    L_SQ_BRACKET = '['
    R_SQ_BRACKET = ']'
    
    DOUBLE_QUOTE = '"'
    SINGLE_QUOTE = "'"
    
    COMMA = ','

class Token:
    def __init__(self, type: TokenTypes, literal: str, line: int, column: int) -> None:
        self.type: TokenTypes = type
        self.literal: str = literal
        
        self.line, self.column = line, column
    
    def __repr__(self) -> str:
        return f'Token({self.type}, {repr(self.literal)}, line={self.line}, column={self.column})'