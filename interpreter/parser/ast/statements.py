# Local imports
from interpreter.parser.ast.expressions import Expression
from interpreter.token import Token
from .node import Node
from .expressions import Expression
from ...token import Token, TokenType

class Statement(Node):
    pass

class DECLARE(Statement):
    def __init__(self, identifier: Token, datatype: Token) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.datatype: Token = datatype
    
    def __str__(self) -> str:
        return f"[DECLARE Statement]: 'DECLARE {self.identifier.literal} : {self.datatype.literal}'"

class DECLARE_ARRAY(DECLARE):
    def __init__(self, identifier: Token, dimensions_sizes: list[Expression], datatype: Token) -> None:
        super().__init__(identifier, datatype)
        
        self.dimensions_sizes: list[tuple[Expression]] = dimensions_sizes
    
    def __str__(self) -> str:
        part: str = ''
        for size in self.dimensions_sizes:
            part += f'1:{str(size)}, '
        return f"[DECLARE ARRAY Statement]: 'DECLARE {self.identifier.literal} : ARRAY[{part[0:-2]}] OF {self.datatype.literal}'"

class CONSTANT(Statement):
    def __init__(self, identifier: Token, value: Token) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.value: Token = value
    
    def __str__(self) -> str:
        return f"[CONSTANT Statement]: 'CONSTANT {self.identifier.literal} = {repr(self.value.literal)}'"

class ASSIGNMENT(Statement):
    def __init__(self, identifier: Token, expression: Expression) -> None:
        super().__init__()
        
        self.identifier: Token = identifier
        self.expression: Expression = expression
    
    def __str__(self) -> str:
        return f"[ASSIGNMENT Statement]: '{self.identifier.literal} <- {str(self.expression)}'"

class ASSIGNMENT_ARRAY(ASSIGNMENT):
    def __init__(self, identifier: Token, indexes: list[Expression], expression: Expression) -> None:
        super().__init__(identifier, expression)
        
        self.indexes: list[Expression] = indexes
    
    def __str__(self) -> str:
        part: str = ''
        for index in self.indexes:
            part += f'{str(index)}, '
        return f"[ASSIGNMENT ARRAY Statement]: '{self.identifier.literal}[{part[0:-2]}] <- {str(self.expression)}'"