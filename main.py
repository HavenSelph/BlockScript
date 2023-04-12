from rich import print
from BlockScript.lexer import Lexer
import BlockScript.Interpreter.values
from BlockScript.Errors.base import SpanError

FILENAME = "local/main.bs"

with open(FILENAME, "r") as f:
    text = f.read()

lexer = Lexer(FILENAME, text)
try:
    print(lexer.lex())
except SpanError as e:
    e.print_error()
