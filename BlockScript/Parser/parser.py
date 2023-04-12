from BlockScript.tokens import Token, TokenKind
from BlockScript.Interpreter.ast import *
from BlockScript.Errors.parser import *


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
        if token.kind == kind:
            self.advance()
            return token
        raise Exception(f"Expected {kind} but got {token.kind}")

    def parse(self) -> Block:
        program = self.parse_block(TokenKind.EOF)
        if self.cur.kind != TokenKind.EOF:
            raise UnexpectedToken(self.cur.span, self.cur.kind, self.cur)
        return program

    def parse_block(self, closer: TokenKind) -> Block:
        statements = []
        start = self.cur.span
        while self.cur.kind != TokenKind.EOF and self.cur.kind != closer:
            statements.append(self.parse_statement())
        return Block(statements, start.extend(self.cur.span))

    def parse_statement(self) -> Node:
        return self.parse_expression()

    def parse_expression(self) -> Node:
        return self.parse_assignment()

    def parse_assignment(self) -> Node:
        return self.parse_logical_or()

    def parse_logical_or(self) -> Node:
        return self.parse_logical_and()

    def parse_logical_and(self) -> Node:
        return self.parse_equality()

    def parse_equality(self) -> Node:
        return self.parse_comparison()

    def parse_comparison(self) -> Node:
        return self.parse_additive()

    def parse_additive(self) -> Node:
        left = self.parse_multiplicative()
        while self.cur.kind in (TokenKind.Plus, TokenKind.Minus):
            match self.cur.kind:
                case TokenKind.Plus:
                    self.advance()
                    right = self.parse_multiplicative()
                    left = Add(left, right, left.span.extend(right.span))
                case TokenKind.Minus:
                    self.advance()
                    right = self.parse_multiplicative()
                    left = Subtract(left, right, left.span.extend(right.span))
        return left

    def parse_multiplicative(self) -> Node:
        return self.parse_prefix()

    def parse_prefix(self) -> Node:
        return self.parse_postfix()

    def parse_postfix(self) -> Node:
        return self.parse_atom()

    def parse_atom(self) -> Node:
        match self.cur.kind:
            case TokenKind.Integer:
                out = IntegerLiteral(self.cur.data, self.cur.span)
                self.advance()
                return out
            case _:
                raise UnexpectedEOF(self.cur.span, "Unexpected EOF")
