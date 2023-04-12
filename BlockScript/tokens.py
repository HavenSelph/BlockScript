from dataclasses import dataclass
from enum import Enum, auto
from .common import Span


class TokenKind(Enum):
    # Misc
    EOF = auto()

    # Keywords
    Let = auto()

    # Symbols
    LeftParen = auto()
    RightParen = auto()

    # Operators
    Plus = auto()
    Minus = auto()

    # Literals
    Identifier = auto()
    Integer = auto()
    Float = auto()
    String = auto()


characters = {
    "(": TokenKind.LeftParen,
    ")": TokenKind.RightParen,
    "+": TokenKind.Plus,
    "-": TokenKind.Minus,
}

keywords = {
    "let": TokenKind.Let,
}


@dataclass
class Token:
    def __init__(self, kind: TokenKind, data: int | float | str | None, span: Span) -> None:
        self.kind = kind
        self.data = data
        self.span = span

    def __str__(self) -> str:
        return f"{self.kind} {self.span}"

    def __repr__(self) -> str:
        return f"Token({self.kind}, {self.data.__repr__()}, {self.span})"
