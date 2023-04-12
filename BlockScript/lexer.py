from .common import Location, Span
from .tokens import Token, TokenKind, characters, keywords
from BlockScript.Errors.base import SpanError


class Lexer:
    def __init__(self, filename: str, text: str) -> None:
        self.filename = filename
        self.text = text
        self.index = 0
        self.line = 1
        self.column = 1
        self.cur = self.text[self.index]
        self.tokens = []

    def location(self, offset: int=0) -> Location:
        return Location(self.filename, self.line, self.column+offset)

    def advance(self, i: int=1) -> None:
        if self.cur == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.index += i
        if self.index >= len(self.text):
            self.cur = None
            return
        self.cur = self.text[self.index]

    def peek(self, i: int) -> str:
        return self.text[self.index + i]

    def push_simple(self, kind: TokenKind, size: int=1) -> None:
        start = self.location()
        self.advance(size)
        end = self.location(offset=-1)
        self.tokens.append(Token(kind, None, Span(start, end)))

    def push(self, kind: TokenKind, data: int | float | str | None, start: Location, end: Location) -> None:
        self.tokens.append(Token(kind, data, Span(start, end)))


    def lex(self) -> list[Token]:
        space = False
        while self.cur:
            match self.cur:
                case "\n":
                    self.advance()
                case char if char.isspace():
                    self.tokens[-1].space_after = True
                    self.advance()
                case char if char.isalpha():
                    self.lex_identifier()
                case char if char.isdigit():
                    self.lex_number()
                case char if char == "." and self.peek(1).isdigit():  # floats that start with .
                    self.lex_number()
                case char if char in characters:
                    self.push_simple(characters[char])
                case _:
                    raise Exception(f"Unexpected character {self.cur}")
        self.push_simple(TokenKind.EOF)
        return self.tokens

    def lex_identifier(self) -> None:
        start = self.location()
        identifier = ""
        while self.cur and (self.cur.isalnum() or self.cur == "_"):
            identifier += self.cur
            self.advance()
        end = self.location(offset=-1)
        kind = keywords.get(identifier, TokenKind.Identifier)
        self.push(kind, identifier, start, end)

    def lex_number(self) -> None:
        start = self.location()
        number = ""
        while self.cur and (self.cur.isdigit() or self.cur == "." or self.cur == "_"):
            if self.cur == "_":
                self.advance()
            if self.cur == "." and "." in number:
                raise Exception("Unexpected character '.'")
            if self.cur == "." and self.peek(1) == "_":
                raise Exception("Unexpected character '_'")
            number += self.cur
            self.advance()
        end = self.location(offset=-1)
        if "." in number:
            self.push(TokenKind.Float, float(number), start, end)
        else:
            self.push(TokenKind.Integer, int(number), start, end)
