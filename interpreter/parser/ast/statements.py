# Local imports
from .node import Node
from .expressions import Expression
from ...token import Token, TokenType

class Statement(Node):
    pass

class DECLARE(Statement):
    def __init__(self, identifier: Token, datatype: TokenType) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.datatype: TokenType = datatype
    
    def __str__(self) -> str:
        return f"[DECLARE Statement]: 'DECLARE {self.identifier.literal} : {self.datatype.value}'"

class DECLARE_ARRAY(DECLARE):
    def __init__(self, identifier: Token, size: tuple[int, int], datatype: TokenType) -> None:
        super().__init__(identifier, datatype)
        
        self.size: tuple[int, int] = size
    
    def __str__(self) -> str:
        return f"[DECLARE ARRAY Statement]: 'DECLARE {self.identifier.literal} : ARRAY[{self.size[0]}:{self.size[1]}] OF {self.datatype.value}'"

class CONSTANT(Statement):
    def __init__(self, identifier: Token) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.expression: Expression
    
    def __str__(self) -> str:
        return f"[CONSTANT Statement]: 'CONSTANT {self.identifier.literal} = ?'"

class ASSIGNMENT(Statement):
    def __init__(self, identifier: Token) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.expression: Expression
    
    def __str__(self) -> str:
        return f"[ASSIGNMENT Statement]: '{self.identifier.literal} <- ?'"