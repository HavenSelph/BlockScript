from rich import print
import BlockScript.Errors.base
from BlockScript.lexer import Lexer
from BlockScript.Parser.parser import Parser
from BlockScript.Interpreter.ast import Scope

FILENAME = "local/main.bs"

with open(FILENAME, "r") as f:
    text = f.read()

try:
    lexer = Lexer(FILENAME, text)
    parser = Parser(lexer.lex())
    ast = parser.parse()
    print(ast.run(Scope()))
except BlockScript.Errors.base.BlockScriptError as e:
    e.print_error()
