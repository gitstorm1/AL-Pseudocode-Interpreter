# Local imports
from ..token import Token, TokenType
from ..lexer import Lexer
from ..errors import ParseError, ExpressionError
from .ast import Node, ParsedProgram, statements, expressions

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
        
        self._parsed_program = ParsedProgram()
    
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
    
    def _parse_DECLARE_ARRAY(self) -> (statements.DECLARE_ARRAY | None):
        # Implement later
        self._skip_remaining_line()
    
    def _parse_DECLARE(self) -> (statements.DECLARE | None):
        if (self._next_token.type != TokenType.IDENTIFIER):
            return self._error(ParseError(TokenType.IDENTIFIER.value, self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        identifier: Token = self._current_token
        
        if (self._next_token.type != TokenType.COLON):
            return self._error(ParseError(TokenType.COLON.value, self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        if (self._next_token.type == TokenType.ARRAY):
            return self._parse_DECLARE_ARRAY()
        if ((self._next_token.type not in self.DATATYPE_TOKEN_TYPES) or (hasattr(self._next_token, 'is_literal'))):
            return self._error(ParseError('a datatype', self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        datatype: TokenType = self._current_token.type
        
        if (TokenType.EOL != self._next_token.type != TokenType.EOF):
            return self._error(ParseError('end of line', self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        return statements.DECLARE(identifier, datatype)
    
    def _parse_CONSTANT(self) -> (statements.CONSTANT | None):
        if (self._next_token.type != TokenType.IDENTIFIER):
            return self._error(ParseError(TokenType.IDENTIFIER.value, self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        identifier: Token = self._current_token
        
        if (self._next_token.type != TokenType.EQUALS_TO):
            return self._error(ParseError(TokenType.EQUALS_TO.value, self._next_token.literal, self._next_token.line, self._next_token.column), skip_line=True)
        self._advance()
        
        # Will implement expression parsing later
        self._skip_remaining_line()
        
        return statements.CONSTANT(identifier)
    
    def _parse_ASSIGNMENT(self) -> (statements.ASSIGNMENT | None):
        identifier: Token = self._current_token
        
        if (self._next_token.type != TokenType.ASSIGNMENT):
            return
        self._advance()
        
        # Will implement expression parsing later
        self._skip_remaining_line()
        
        return statements.ASSIGNMENT(identifier)
    
    def _parse_statement(self) -> (statements.Statement | None):
        match(self._current_token.type):
            case TokenType.DECLARE:
                return self._parse_DECLARE()
            case TokenType.CONSTANT:
                return self._parse_CONSTANT()
            case TokenType.IDENTIFIER:
                return self._parse_ASSIGNMENT()
    
    def _parse_expression(self) -> expressions.Expression:
        lhs: expressions.Expression
        match(self._current_token.type):
            case TokenType.INTEGER:
                lhs = expressions.Atom(self._current_token)
            case TokenType.REAL:
                lhs = expressions.Atom(self._current_token)
            case TokenType.IDENTIFIER:
                lhs = expressions.Atom(self._current_token)
            case _:
                raise ExpressionError(self._current_token.line, self._current_token.column)
        
        self._advance()
        
        match(self._current_token.type):
            case TokenType.PLUS:
                self._advance()
                rhs: expressions.Expression = self._parse_expression()
                lhs = expressions.BinaryOperator(TokenType.PLUS, lhs, rhs)
        
        return lhs
    
    def parse_program(self) -> ParsedProgram:
        parsed_program = self._parsed_program
        
        while (self._current_token.type != TokenType.EOF):
            statement: (statements.Statement | None) = self._parse_statement()
            
            if (statement):
                parsed_program.statements.append(statement)
            elif (TokenType.EOL != self._current_token.type != TokenType.EOF):
                print(self._parse_expression())
            
            self._advance()
        
        return parsed_program