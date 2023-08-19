# Standard library imports
import cmd, enum

# Local imports
from .lexer.lexer import Lexer, Token, TokenType

def output_tokens(input: str) -> None:
    lexer = Lexer(input)
    
    try:
        token: Token = lexer.get_next_token()
        while (token.type != TokenType.EOF):
            print(token)
            token = lexer.get_next_token()
        print(token)
    except Exception as error:
        print(error)

class ShellState(enum.Enum):
    NORMAL = '>>> '
    MULTI_LINE_INPUT = '... '

class Repl(cmd.Cmd):
    intro: str = """Welcome to the A-Level Pseudocode shell. Type 'help' or '?' for a list of commands.
For a multi-line input, add a backslash ('\\') at the end of each line input."""
    prompt: str = ShellState.NORMAL.value
    
    state: ShellState = ShellState.NORMAL
    stored_input: str = ""
    
    def do_exit(self, arg: str):
        "Exits out of the shell."
        exit()
    
    def do_exec(self, arg: str):
        "Executes the script located at the path specified."
        print("--Not yet implemented--")
    
    def emptyline(self):
        return self.default('')
    
    def default(self, line: str):
        if ((len(line) != 0) and (line[-1] == '\\')):
            if (self.state == ShellState.NORMAL):
                self.state = ShellState.MULTI_LINE_INPUT
                self.prompt = self.state.value
                
                self.stored_input = line[0 : -1]
                
                return
            
            self.stored_input += ('\n' + line[0 : -1])
            
            return
        
        if (self.state == ShellState.MULTI_LINE_INPUT):
            self.state = ShellState.NORMAL
            self.prompt = self.state.value
            
            self.stored_input += ('\n' + line)
            output_tokens(self.stored_input)
            
            return
            
        output_tokens(line)