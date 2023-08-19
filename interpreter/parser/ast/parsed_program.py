# Local imports
from .node import Node
from .statements import Statement

class ParsedProgram(Node):
    def __init__(self) -> None:
        super().__init__()
        self.statements: list[Statement] = []