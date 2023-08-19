class PseudocodeError(Exception):
    pass

class LexerError(PseudocodeError):
    def __init__(self, message: str) -> None:
        super().__init__('LexerError: ' + message)

class ParserError(PseudocodeError):
    def __init__(self, message: str) -> None:
        super().__init__('ParserError: ' + message)