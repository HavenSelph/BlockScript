from rich import print
from BlockScript.lexer import Lexer
import BlockScript.Interpreter.values
from BlockScript.Errors.base import SpanError

FILENAME = "local/main.bs"

with open(FILENAME, "r") as f:
    text = f.read()

lexer = Lexer(FILENAME, text)
tokens = lexer.lex()
SpanError(
    tokens[-1].span,
    "This is a test error",
).print_error()

print(tokens)
