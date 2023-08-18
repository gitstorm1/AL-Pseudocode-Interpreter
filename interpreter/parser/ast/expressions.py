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

class PrefixOperator(Expression):
    def __init__(self, operator: Token, operand: Token) -> None:
        super().__init__()
        self.operator: Token = operator
        self.operand: Expression = operand
    def __str__(self) -> str:
        return f"({self.operator.type.value}{str(self.operand)})"

class InfixOperator(Expression):
    def __init__(self, operator: Token, lhs: Expression, rhs: Expression) -> None:
        super().__init__()
        self.operator: Token = operator
        self.lhs: Expression = lhs
        self.rhs: Expression = rhs
    def __str__(self) -> str:
        return f"({str(self.lhs)}{'' if (self.operator.type == TokenType.L_PARENTHESES) else self.operator.type.value}{str(self.rhs)})"

class PostfixOperator(Expression):
    def __init__(self, operand: Expression, operator: Token) -> None:
        super().__init__()
        self.operand: Expression = operand
        self.operator: Token = operator
    def __str__(self) -> str:
        return f"({str(self.operand)}{self.operator.type.value})"