# Standard library imports
from enum import Enum

# Local imports
from ..token import Token, TokenType
from ..lexer import Lexer
from ..errors import ParserError
from .ast import ParsedProgram, statements, expressions

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
        
        TokenType.PERIOD: (21, 20),
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
    
    #def _skip_remaining_line(self) -> None:
    #    while (TokenType.EOL != self._current_token.type != TokenType.EOF):
    #        self._advance()
    #    else:
    #        self._advance()
    
    def _parse_statement_DECLARE_ARRAY(self, identifier: Token) -> statements.DECLARE_ARRAY:
        self._advance()
        
        if (self._current_token.type != TokenType.L_SQ_BRACKET):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.L_SQ_BRACKET.value)}, got {repr(self._current_token.literal)}")
        
        self._advance()
        
        dimensions_sizes: list[expressions.Expression] = []
        
        while True:
            if (self._current_token.literal != '1'):
                raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected '{1}', got {repr(self._current_token.literal)}")
            
            self._advance()
            
            if (self._current_token.type != TokenType.COLON):
                raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.COLON.value)}, got {repr(self._current_token.literal)}")
            
            self._advance()
            
            dimensions_sizes.append(self._parse_expression(0))
            
            if (self._current_token.type == TokenType.COMMA):
                self._advance()
                continue
            
            if (self._current_token.type != TokenType.R_SQ_BRACKET):
                raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.R_SQ_BRACKET.value)}, got {repr(self._current_token.literal)}")
            
            self._advance()
            break
        
        if (self._current_token.type != TokenType.OF):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.OF.value)}, got {repr(self._current_token.literal)}")
        
        self._advance()
        
        match(self._current_token.type):
            case TokenType.INTEGER | TokenType.REAL | TokenType.CHAR | TokenType.STRING | TokenType.BOOLEAN | TokenType.DATE | TokenType.IDENTIFIER:
                datatype: Token = self._current_token
                
                self._advance()
                
                if (TokenType.EOL != self._current_token.type != TokenType.EOF):
                    raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected the line to end")
                
                self._advance()
                
                return statements.DECLARE_ARRAY(identifier, dimensions_sizes, datatype)
        
        raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected a datatype, got {repr(self._current_token.literal)}")
    
    def _parse_statement_DECLARE(self) -> statements.DECLARE:
        self._advance()
        
        if (self._current_token.type != TokenType.IDENTIFIER):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected identifier, got {repr(self._current_token.literal)}")
        
        identifier: Token = self._current_token
        
        self._advance()
        
        if (self._current_token.type != TokenType.COLON):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.COLON.value)}, got {repr(self._current_token.literal)}")
        
        self._advance()
        
        if (self._current_token.type == TokenType.ARRAY):
            return self._parse_statement_DECLARE_ARRAY(identifier)
        
        match(self._current_token.type):
            case TokenType.INTEGER | TokenType.REAL | TokenType.CHAR | TokenType.STRING | TokenType.BOOLEAN | TokenType.DATE | TokenType.IDENTIFIER:
                datatype: Token = self._current_token
                
                self._advance()
                
                if (TokenType.EOL != self._current_token.type != TokenType.EOF):
                    raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected the line to end")
                
                self._advance()
                
                return statements.DECLARE(identifier, datatype)
        
        raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected a datatype, got {repr(self._current_token.literal)}")
    
    def _parse_statement_CONSTANT(self) -> statements.CONSTANT:
        self._advance()
        
        if (self._current_token.type != TokenType.IDENTIFIER):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected identifier, got {repr(self._current_token.literal)}")
        
        identifier: Token = self._current_token
        
        self._advance()
        
        if (self._current_token.type != TokenType.EQUALS_TO):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.EQUALS_TO.value)}, got {repr(self._current_token.literal)}")
        
        self._advance()
        
        match(self._current_token.type):
            case TokenType.INTEGER | TokenType.REAL | TokenType.CHAR | TokenType.STRING | TokenType.BOOLEAN | TokenType.DATE:
                if (hasattr(self._current_token, 'is_literal')):
                    value: Token = self._current_token
                    
                    self._advance()
                    
                    if (TokenType.EOL != self._current_token.type != TokenType.EOF):
                        raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected the line to end")
                    
                    self._advance()
                    
                    return statements.CONSTANT(identifier, value)
        
        raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected a literal, got {repr(self._current_token.literal)}")
    
    def _parse_statement_ASSIGNMENT_ARRAY(self, identifier: Token) -> statements.ASSIGNMENT_ARRAY:
        self._advance()
        
        indexes: list[expressions.Expression] = [self._parse_expression(0)]
        
        while (self._current_token.type == TokenType.COMMA):
            self._advance()
            indexes.append(self._parse_expression(0))
        
        if (self._current_token.type != TokenType.R_SQ_BRACKET):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.R_SQ_BRACKET.value)}, got {repr(self._current_token.literal)}")

        self._advance()
        
        if (self._current_token.type != TokenType.ASSIGNMENT):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.ASSIGNMENT.value)}, got {repr(self._current_token.literal)}")
        
        self._advance()
        
        expression: expressions.Expression = self._parse_expression(0)
        
        if (TokenType.EOL != self._current_token.type != TokenType.EOF):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected the line to end")
        
        self._advance()
        
        return statements.ASSIGNMENT_ARRAY(identifier, indexes, expression)
    
    
    def _parse_statement_ASSIGNMENT(self) -> statements.ASSIGNMENT:
        identifier: Token = self._current_token
        
        self._advance()
        
        if (self._current_token.type == TokenType.L_SQ_BRACKET):
            return self._parse_statement_ASSIGNMENT_ARRAY(identifier)
        
        if (self._current_token.type != TokenType.ASSIGNMENT):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.ASSIGNMENT.value)}, got {repr(self._current_token.literal)}")
        
        self._advance()
        
        expression: expressions.Expression = self._parse_expression(0)
        
        if (TokenType.EOL != self._current_token.type != TokenType.EOF):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected the line to end")
        
        self._advance()
        
        return statements.ASSIGNMENT(identifier, expression)
    
    def _parse_statement_INPUT(self) -> statements.INPUT:
        self._advance()
        
        if (self._current_token.type != TokenType.IDENTIFIER):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected {repr(TokenType.IDENTIFIER.value)}, got {repr(self._current_token.literal)}")

        identifier: Token = self._current_token
        
        self._advance()
        
        if (TokenType.EOL != self._current_token.type != TokenType.EOF):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; expected the line to end")
        
        return statements.INPUT(identifier)
        
    def _parse_statement(self) -> (statements.Statement | None):
        match(self._current_token.type):
            case TokenType.DECLARE:
                return self._parse_statement_DECLARE()
            case TokenType.CONSTANT:
                return self._parse_statement_CONSTANT()
            case TokenType.IDENTIFIER:
                return self._parse_statement_ASSIGNMENT()
            case TokenType.INPUT:
                return self._parse_statement_INPUT()
        return None
    
    def _parse_expression_atom(self) -> (expressions.Atom | None):
        current_token: Token = self._current_token
        
        match(current_token.type):
            case TokenType.IDENTIFIER:
                self._advance()
                return expressions.Atom(current_token)
            case TokenType.INTEGER | TokenType.REAL | TokenType.CHAR | TokenType.STRING | TokenType.BOOLEAN | TokenType.DATE:
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
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; unclosed parenthesis")
        
        self._advance()
        return parenthesized_expr
    
    def _parse_expression_function_call(self, identifier: expressions.Expression) -> expressions.FunctionCall:
        if ((not isinstance(identifier, expressions.Atom)) or (identifier.token.type != TokenType.IDENTIFIER)):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; it must be a plain function identifier")
        
        arguments: list[expressions.Expression] = []
        
        self._advance()
        if (self._current_token.type != TokenType.R_PARENTHESES):
            arguments.append(self._parse_expression(0))
            
            while (self._current_token.type == TokenType.COMMA):
                self._advance()
                arguments.append(self._parse_expression(0))
            
            if (self._current_token.type != TokenType.R_PARENTHESES):
                raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; unclosed parenthesis")
        
        self._advance()
        return expressions.FunctionCall(identifier, arguments)
    
    def _parse_expression_array_indexing(self, identifier: expressions.Expression) -> expressions.ArrayIndexing:
        if ((not isinstance(identifier, expressions.Atom)) or (identifier.token.type != TokenType.IDENTIFIER)):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; it must be a plain array identifier")
        
        self._advance()
        indexes: list[expressions.Expression] = [self._parse_expression(0)]
        
        while (self._current_token.type == TokenType.COMMA):
            self._advance()
            indexes.append(self._parse_expression(0))
        
        if (self._current_token.type != TokenType.R_SQ_BRACKET):
            raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; unclosed square brackets")
        
        self._advance()
        return expressions.ArrayIndexing(identifier, indexes)
    
    def _parse_expression(self, other_bp: int) -> expressions.Expression:
        lhs: (expressions.Expression | None) = self._parse_expression_atom()
        if (not lhs):
            lhs = self._parse_expression_prefix()
            if (not lhs):
                lhs = self._parse_expression_enclosing_parentheses()
                if (not lhs):
                    raise ParserError(f"line {self._current_token.line}, col {self._current_token.column}; unexpected token {repr(self._current_token.literal)}")
        
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
                raise ParserError(f"line {self._current_token.line}; invalid statement")
            else:
                self._advance()
        
        return parsed_program