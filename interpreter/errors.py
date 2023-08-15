class Error(Exception):
    pass

class ParseError(Error):
    def __init__(self, expected: str, got: str, line: int, column: int) -> None:
        super().__init__(f"[ParseError]: line {line}, col {column}; expected {expected}, got {got}")
        self.line, self.column = line, column