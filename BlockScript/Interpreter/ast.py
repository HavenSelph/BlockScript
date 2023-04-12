from __future__ import annotations
from abc import ABC, abstractmethod
from BlockScript.common import Span, Location
from BlockScript.Interpreter.values import Value


class Program:
    def __init__(self, nodes: list[Node]) -> None:
        self.nodes = nodes

    def __repr__(self) -> str:
        return f"Program({self.nodes})"

    def run(self, ctx) -> Value:
        pass


class Node(ABC):
    def __init__(self, span: Span) -> None:
        self.span = span

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def run(self, ctx) -> Value:
        pass


class Add(Node):
    def __init__(self, left: Node, right: Node, span: Span) -> None:
        super().__init__(span)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"AddNode({self.left}, {self.right}, {self.span})"

    def run(self, ctx) -> Value:
        return self.left.run(ctx).add(self.right.run(ctx))
