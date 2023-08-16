# Local imports
from .node import Node
from .statements import Statement
from ...errors import Error

class ParsedProgram(Node):
    def __init__(self) -> None:
        super().__init__()
        
        self.errors: list[Error] = []
        
        self.statements: list[Statement] = []