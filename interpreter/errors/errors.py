class Error(Exception):
    pass

class ParseError(Error):
    def __init__(self, expected: str, got: str, line: int, column: int) -> None:
        super().__init__(f"line {line}, col {column}; expected {expected}, got {got}")
        self.line, self.column = line, column

class ExpressionError(Error):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(f"line {line}, col {column}; unexpected token")
        self.line, self.column = line, column