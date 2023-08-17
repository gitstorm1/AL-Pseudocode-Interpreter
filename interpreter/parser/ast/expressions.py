# Local imports
from ...token import Token, TokenType
from .node import Node

class Expression(Node):
    def __init__(self) -> None:
        super().__init__()
        
        

class Atom(Expression):
    def __init__(self, token: Token) -> None:
        super().__init__()
        self.token: Token = token
    
    def __str__(self) -> str:
        return self.token.literal
    
class BinaryOperator(Expression):
    def __init__(self, operator: TokenType, lhs: Expression, rhs: Expression) -> None:
        super().__init__()
        self.operator: TokenType = operator
        self.lhs: Expression = lhs
        self.rhs: Expression = rhs
    def __str__(self) -> str:
        return f"({str(self.lhs)} {self.operator.value} {str(self.rhs)})"