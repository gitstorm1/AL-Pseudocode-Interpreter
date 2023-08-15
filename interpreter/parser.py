# Local imports
from .lexer import Lexer, Token, TokenType
from .errors import ParseError
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
        
        self._parsed_program = ast.ParsedProgram()
    
    def _advance(self) -> None:
        self._current_token: Token = self._next_token
        self._next_token: Token = self._lexer.get_next_token()
    
    def _skip_remaining_line(self) -> None:
        while (TokenType.EOL != self._current_token.type != TokenType.EOF):
            self._advance()
    
    def _error(self, error: ParseError, skip_line: bool) -> None:
        self._parsed_program.errors.append(error)
        if (skip_line):
            self._skip_remaining_line()
    
    def _parse_DECLARE(self) -> (ast.DECLARE_statement | None):
        if (self._next_token.type != TokenType.IDENTIFIER):
            return self._error(ParseError(TokenType.IDENTIFIER.value, self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        identifier: Token = self._current_token
        
        if (self._next_token.type != TokenType.COLON):
            return self._error(ParseError(TokenType.COLON.value, self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        if ((self._next_token.type not in self.DATATYPE_TOKEN_TYPES) or (hasattr(self._next_token, 'is_literal'))):
            return self._error(ParseError('a datatype', self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        datatype: TokenType = self._current_token.type
        
        if (TokenType.EOL != self._next_token.type != TokenType.EOF):
            return self._error(ParseError('end of line', self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        return ast.DECLARE_statement(identifier, datatype)
    
    def _parse_statement(self) -> (ast.Statement | None):
        match(self._current_token.type):
            case TokenType.DECLARE:
                return self._parse_DECLARE()
    
    def _parse_expression(self):
        pass
    
    def parse_program(self) -> ast.ParsedProgram:
        parsed_program = self._parsed_program
        
        while (self._current_token.type != TokenType.EOF):
            statement: (ast.Statement | None) = self._parse_statement()
            
            if (statement):
                parsed_program.statements.append(statement)
            elif (TokenType.EOL != self._current_token.type != TokenType.EOF):
                print("Parse as an expression instead:", self._current_token)
            
            self._advance()
        
        return parsed_program