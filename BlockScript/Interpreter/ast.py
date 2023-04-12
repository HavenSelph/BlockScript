from __future__ import annotations
from BlockScript.Interpreter.values import *


class Scope:
    def __init__(self, parent: Scope | None = None, in_function: bool=False) -> None:
        """
        todo: it is possible that closures will cause huge memory leaks, should check this
        """
        self.parent = parent
        self.in_function = in_function
        self.variables: dict[str, Value] = {}

    def __repr__(self) -> str:
        return f"Scope({self.parent}, {self.variables})"

    def get(self, name: str) -> Value:
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            self.parent.get(name)
        else:
            raise KeyError(f"Variable {name} not found")

    def set(self, name: str, value: Value) -> None:
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise KeyError(f"Variable {name} not found")

    def define(self, name: str, value: Value) -> None:
        self.variables[name] = value


"""
CONTROL FLOW EXCEPTIONS
"""


class ControlFlow(Exception):
    def __init__(self, value: Value) -> None:
        self.value = value


class Return(ControlFlow):
    def __init__(self, value: Value) -> None:
        super().__init__(value)


class Break(ControlFlow):
    def __init__(self, value: Value=Null()) -> None:
        super().__init__(value)


class Continue(ControlFlow):
    def __init__(self, value: Value=Null()) -> None:
        super().__init__(value)


"""
AST NODES
"""


class Node(ABC):
    def __init__(self, span: Span) -> None:
        self.span = span

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def run(self, scope: Scope) -> Value:
        pass


class Block(Node):
    def __init__(self, statements: list[Node], span: Span) -> None:
        super().__init__(span)
        self.statements = statements

    def __repr__(self) -> str:
        return f"BlockNode({self.statements}, {self.span})"

    def run(self, scope: Scope, new_scope=True) -> Value:
        if new_scope:
            scope = Scope(scope)
        out = Null()  # Default return value
        try:
            for statement in self.statements:
                out = statement.run(scope)
        except Return as ret:
            out = ret.value
        return out


class IntegerLiteral(Node):
    def __init__(self, value: int, span: Span) -> None:
        super().__init__(span)
        self.value = value

    def __repr__(self) -> str:
        return f"IntegerLiteralNode({self.value}, {self.span})"

    def run(self, scope: Scope) -> Value:
        return Integer(self.value)


class FloatLiteral(Node):
    def __init__(self, value: float, span: Span) -> None:
        super().__init__(span)
        self.value = value

    def __repr__(self) -> str:
        return f"FloatLiteralNode({self.value}, {self.span})"

    def run(self, scope: Scope) -> Value:
        return Float(self.value)


class StringLiteral(Node):
    def __init__(self, value: str, span: Span) -> None:
        super().__init__(span)
        self.value = value

    def __repr__(self) -> str:
        return f"StringLiteralNode({self.value}, {self.span})"

    def run(self, scope: Scope) -> Value:
        return String(self.value)


class Add(Node):
    def __init__(self, left: Node, right: Node, span: Span) -> None:
        super().__init__(span)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"AddNode({self.left}, {self.right}, {self.span})"

    def run(self, scope: Scope) -> Value:
        return self.left.run(scope).add(self.right.run(scope), self.span)


class Subtract(Node):
    def __init__(self, left: Node, right: Node, span: Span) -> None:
        super().__init__(span)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"SubtractNode({self.left}, {self.right}, {self.span})"

    def run(self, scope: Scope) -> Value:
        return self.left.run(scope).subtract(self.right.run(scope), self.span)
