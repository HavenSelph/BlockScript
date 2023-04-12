from __future__ import annotations
from .values import Value


class Scope:
    def __init__(self, parent: Scope | None = None) -> None:
        self.parent = parent
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
