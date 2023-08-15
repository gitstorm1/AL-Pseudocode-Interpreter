from .token import Token, TokenType

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
        return f"'''DECLARE {self.identifier.literal} : {self.datatype.value}'''"

class Program(Node):
    def __init__(self) -> None:
        super().__init__()
        
        self.statements: list[Statement] = []