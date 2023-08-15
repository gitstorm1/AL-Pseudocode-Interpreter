# Local imports
from .lexer import Lexer, Token, TokenType

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        
        self._current_token: Token = lexer.get_next_token()
        self._next_token: Token = lexer.get_next_token()
    
    def _advance(self):
        self._current_token: Token = self._next_token
        self._next_token: Token = self._lexer.get_next_token()
    
    def _parse_DECLARE(self):
        print("Parse DECLARE statement.")
    
    def parse_program(self):
        self._advance()
        
        while (self._current_token.type != TokenType.EOF):
            if (self._current_token.type == TokenType.DECLARE):
                self._parse_DECLARE()
            
            self._advance()