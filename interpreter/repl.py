# Standard library imports
import cmd

# Local imports
from .lexer import Lexer, Token, TokenTypes

def output_tokens(input: str) -> None:
    lexer = Lexer(input)
    
    # The EOF token is intentionally not printed
    token: Token = lexer.get_next_token()
    while (token.type != TokenTypes.EOF):
        print(token)
        token = lexer.get_next_token()

class Repl(cmd.Cmd):
    intro = "Welcome to the A-Level Pseudocode shell. Type 'help' or '?' for a list of commands."
    prompt = '>>> '
    
    def do_exit(self, arg: str):
        "This command exits out of the shell."
        exit()
    
    def default(self, line: str):
        output_tokens(line)