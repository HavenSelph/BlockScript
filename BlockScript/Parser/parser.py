from BlockScript.tokens import Token, TokenKind
from BlockScript.Interpreter.ast import *


class Parser:
    def __init__(self, tokens: list[Token]):
        self.filename = tokens[0].span.start.filename
        self.tokens = tokens
        self.index = 0
        self.cur = self.tokens[self.index]

    def advance(self, i: int=1) -> None:
        if self.cur == TokenKind.EOF:
            return
        self.index += i
        self.cur = self.tokens[self.index]

    def consume(self, kind: TokenKind, expect_whitespace: bool=False) -> Token:
        if expect_whitespace and not self.cur.space_after:
            raise Exception(f"Expected whitespace after {self.cur.kind} but got {self.cur.kind} without whitespace")
        token = self.cur
        if token == kind:
            self.advance()
            return token
        raise Exception(f"Expected {kind} but got {token.kind}")

    def parse(self) -> Program:
