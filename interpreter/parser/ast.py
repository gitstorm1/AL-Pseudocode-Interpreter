from ..token.token import Token, TokenType
from ..errors.errors import Error

class Node:
    pass

class Statement(Node):
    pass

class DECLARE_statement(Statement):
    def __init__(self, identifier: Token, datatype: TokenType) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.datatype: TokenType = datatype
    
    def __str__(self) -> str:
        return f"[DECLARE Statement]: 'DECLARE {self.identifier.literal} : {self.datatype.value}'"

class ASSIGNMENT_statement(Statement):
    def __init__(self, identifier: Token) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        # self.expression: Token = value
    
    def __str__(self) -> str:
        return f"[ASSIGNMENT Statement]: '{self.identifier.literal} {TokenType.ASSIGNMENT.value} ?'"

class ParsedProgram(Node):
    def __init__(self) -> None:
        super().__init__()
        
        self.errors: list[Error] = []
        
        self.statements: list[Statement] = []