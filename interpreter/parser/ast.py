from interpreter.token.token import Token, TokenType
from ..token.token import Token, TokenType
from ..errors.errors import Error

class Node:
    pass

class Statement(Node):
    pass

class Expression(Node):
    pass

class DECLARE_statement(Statement):
    def __init__(self, identifier: Token, datatype: TokenType) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.datatype: TokenType = datatype
    
    def __str__(self) -> str:
        return f"[DECLARE Statement]: 'DECLARE {self.identifier.literal} : {self.datatype.value}'"

class DECLARE_ARRAY_statement(DECLARE_statement):
    def __init__(self, identifier: Token, size: tuple[int, int], datatype: TokenType) -> None:
        super().__init__(identifier, datatype)
        
        self.size: tuple[int, int] = size
    
    def __str__(self) -> str:
        return f"[DECLARE ARRAY Statement]: 'DECLARE {self.identifier.literal} : ARRAY[{self.size[0]}:{self.size[1]}] OF {self.datatype.value}'"

class CONSTANT_statement(Statement):
    def __init__(self, identifier: Token) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.expression: Expression
    
    def __str__(self) -> str:
        return f"[CONSTANT Statement]: 'CONSTANT {self.identifier.literal} = ?'"

class ASSIGNMENT_statement(Statement):
    def __init__(self, identifier: Token) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.expression: Expression
    
    def __str__(self) -> str:
        return f"[ASSIGNMENT Statement]: '{self.identifier.literal} <- ?'"

class ParsedProgram(Node):
    def __init__(self) -> None:
        super().__init__()
        
        self.errors: list[Error] = []
        
        self.statements: list[Statement] = []