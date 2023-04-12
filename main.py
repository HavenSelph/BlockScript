from rich import print
from BlockScript.lexer import Lexer


lexer = Lexer("main.bs", "1 + 2 \n3+4")
print(lexer.lex())
