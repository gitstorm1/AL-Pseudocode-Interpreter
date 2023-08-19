# Standard library imports
from enum import Enum

# Local imports
from ..token import Token, TokenType
from ..lexer import Lexer
from ..errors import ParseError, ExpressionError
from .ast import Node, ParsedProgram, statements, expressions

binding_powers = {
    'prefix': {
        TokenType.HYPHEN: ((), 17),
        TokenType.NOT: ((), 5)
    },
    'infix': {
        TokenType.AMPERSAND: (1, 2),
        
        TokenType.OR: (3, 4),
        TokenType.AND: (3, 4),
        
        TokenType.EQUALS_TO: (7, 8),
        TokenType.NOT_EQUALS_TO: (9, 10),
        
        TokenType.L_ANGLE_BRACKET: (11, 12),
        TokenType.LESSER_OR_EQUALS_TO: (11, 12),
        TokenType.R_ANGLE_BRACKET: (11, 12),
        TokenType.GREATER_OR_EQUALS_TO: (11, 12),
        
        TokenType.PLUS: (13, 14),
        TokenType.HYPHEN: (13, 14),
    
        TokenType.ASTERISK: (15, 16),
        TokenType.FORWARD_SLASH: (15, 16),
        TokenType.INT_DIV: (15, 16),
        TokenType.MODULUS: (15, 16),
        
        TokenType.CARET: (19, 18),
        
        TokenType.PERIOD: (20, 21),
    },
    'postfix': {
    },
}

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
    
    def _parse_expression_atom(self) -> (expressions.Atom | None):
        current_token: Token = self._current_token
        
        match(current_token.type):
            case TokenType.INTEGER | TokenType.REAL | TokenType.IDENTIFIER:
                self._advance()
                return expressions.Atom(current_token)
            case TokenType.STRING:
                if (hasattr(current_token, 'is_literal')):
                    self._advance()
                    return expressions.Atom(current_token) 

        return None
    
    def _parse_expression_prefix(self) -> (expressions.PrefixOperator | None):
        operator: Token = self._current_token
        
        bp: (tuple[None, int] | None) = binding_powers['prefix'].get(operator.type)
        
        # Not a prefix operator
        if (not bp):
            return None
        
        self._advance()
        return expressions.PrefixOperator(operator, operand=self._parse_expression(bp[1]))
    
    def _parse_expression_enclosing_parentheses(self) -> (expressions.Expression | None):
        if (self._current_token.type != TokenType.L_PARENTHESES):
            return None
        
        self._advance()
        parenthesized_expr: expressions.Expression = self._parse_expression(0)
        
        if (self._current_token.type != TokenType.R_PARENTHESES):
            return None # Error
        
        self._advance()
        return parenthesized_expr
    
    def _parse_expression_function_call(self, identifier: expressions.Expression) -> expressions.FunctionCall:
        if ((not isinstance(identifier, expressions.Atom)) or (identifier.token.type != TokenType.IDENTIFIER)):
            raise ParseError('function identifier', 'something else', self._current_token.line, self._current_token.column)
        
        arguments: list[expressions.Expression] = []
        
        self._advance()
        if (self._current_token.type != TokenType.R_PARENTHESES):
            arguments.append(self._parse_expression(0))
            
            while (self._current_token.type == TokenType.COMMA):
                self._advance()
                arguments.append(self._parse_expression(0))
            
            if (self._current_token.type != TokenType.R_PARENTHESES):
                raise ExpressionError(self._current_token.line, self._current_token.column, self._current_token.literal)
        
        self._advance()
        return expressions.FunctionCall(identifier, arguments)
    
    def _parse_expression_array_indexing(self, identifier: expressions.Expression) -> expressions.ArrayIndexing:
        if ((not isinstance(identifier, expressions.Atom)) or (identifier.token.type != TokenType.IDENTIFIER)):
            raise ParseError('array identifier', 'something else', self._current_token.line, self._current_token.column)
        
        self._advance()
        indexes: list[expressions.Expression] = [self._parse_expression(0)]
        
        while (self._current_token.type == TokenType.COMMA):
            self._advance()
            indexes.append(self._parse_expression(0))
        
        if (self._current_token.type != TokenType.R_SQ_BRACKET):
            raise ExpressionError(self._current_token.line, self._current_token.column, self._current_token.literal)
        
        self._advance()
        return expressions.ArrayIndexing(identifier, indexes)
    
    def _parse_expression(self, other_bp: int) -> expressions.Expression:
        lhs: (expressions.Expression | None) = self._parse_expression_atom()
        if (not lhs):
            lhs = self._parse_expression_prefix()
            if (not lhs):
                lhs = self._parse_expression_enclosing_parentheses()
                if (not lhs):
                    raise ExpressionError(self._current_token.line, self._current_token.column, self._current_token.literal)
        
        while (TokenType.EOL != self._current_token.type != TokenType.EOF):
            operator: Token = self._current_token
            
            if (operator.type == TokenType.L_PARENTHESES):
                lhs = self._parse_expression_function_call(identifier=lhs)
                continue
            
            if (operator.type == TokenType.L_SQ_BRACKET):
                lhs = self._parse_expression_array_indexing(identifier=lhs)
                continue
            
            bp: (tuple[int, int] | None) = binding_powers['infix'].get(operator.type)
            if ((not bp) or (other_bp >= bp[0])):
                break
            
            self._advance()
            lhs = expressions.InfixOperator(operator, lhs, rhs=self._parse_expression(bp[1]))
        
        return lhs
    
    def parse_program(self) -> ParsedProgram:
        parsed_program = self._parsed_program
        
        while (self._current_token.type != TokenType.EOF):
            statement: (statements.Statement | None) = self._parse_statement()
            
            if (statement):
                parsed_program.statements.append(statement)
            elif (TokenType.EOL != self._current_token.type != TokenType.EOF):
                print(self._parse_expression(0))
                if (TokenType.EOL != self._current_token.type != TokenType.EOF):
                    print("Error.")
                self._skip_remaining_line()
            
            self._advance()
        
        return parsed_program