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
        if (self.token.type == TokenType.STRING):
            return f'"{self.token.literal}"'
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
        return f"({str(self.lhs)} {self.operator.type.value} {str(self.rhs)})"

class FunctionCall(Expression):
    def __init__(self, identifier: Expression, arguments: list[Expression]) -> None:
        super().__init__()
        self.identifier: Expression = identifier
        self.arguments: list[Expression] = arguments
    def __str__(self) -> str:
        args: str = ''
        for arg in self.arguments:
            args += str(arg) + ', '
        return f"{str(self.identifier)}({args[0:-2]})"

class ArrayIndexing(Expression):
    def __init__(self, identifier: Expression, indexes: list[Expression]) -> None:
        super().__init__()
        self.identifier: Expression = identifier
        self.indexes: list[Expression] = indexes
    def __str__(self) -> str:
        indexes: str = ''
        for index in self.indexes:
            indexes += str(index) + ', '
        return f"{str(self.identifier)}[{indexes[0:-2]}]"

class PostfixOperator(Expression):
    def __init__(self, operand: Expression, operator: Token) -> None:
        super().__init__()
        self.operand: Expression = operand
        self.operator: Token = operator
    def __str__(self) -> str:
        return f"({str(self.operand)}{self.operator.type.value})"