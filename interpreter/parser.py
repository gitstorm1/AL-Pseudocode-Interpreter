# Local imports
from .lexer import Lexer, Token, TokenType
from . import ast

class Parser:
    DATATYPE_TOKEN_TYPES: list[TokenType] = [
        TokenType.INTEGER, 
        TokenType.REAL, 
        TokenType.CHAR,
        TokenType.STRING,
        TokenType.BOOLEAN,
        TokenType.DATE
    ]
    
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        
        self._current_token: Token = lexer.get_next_token()
        self._next_token: Token = lexer.get_next_token()
    
    def _advance(self):
        self._current_token: Token = self._next_token
        self._next_token: Token = self._lexer.get_next_token()
    
    def _parse_DECLARE(self) -> (ast.DECLARE_statement | None):
        if (self._next_token.type != TokenType.IDENTIFIER):
            print(f"[ParseError] line {self._next_token.line}, col {self._next_token.column}; expected {TokenType.IDENTIFIER.value}, got {repr(self._next_token.literal)}")
            return
        self._advance()
        
        identifier: Token = self._current_token
        
        if (self._next_token.type != TokenType.COLON):
            print(f"[ParseError] line {self._next_token.line}, col {self._next_token.column}; expected {TokenType.COLON.value}, got {repr(self._next_token.literal)}")
            return
        self._advance()
        
        if ((self._next_token.type not in self.DATATYPE_TOKEN_TYPES) or (hasattr(self._next_token, 'is_literal'))):
            print(f"[ParseError] line {self._next_token.line}, col {self._next_token.column}; expected a datatype, got {repr(self._next_token.literal)}")
            return
        self._advance()
        
        datatype: TokenType = self._current_token.type
        
        return ast.DECLARE_statement(identifier, datatype)
    
    def parse_program(self) -> ast.Program:
        program = ast.Program()
        
        self._advance()
        
        while (self._current_token.type != TokenType.EOF):
            statement: (ast.Statement | None) = None
            
            if (self._current_token.type == TokenType.DECLARE):
                statement = self._parse_DECLARE()
            
            if (statement):
                program.statements.append(statement)
            
            self._advance()
        
        return program