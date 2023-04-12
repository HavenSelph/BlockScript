from __future__ import annotations
from abc import ABC, abstractmethod


class Value(ABC):
    def __init__(self, value) -> None:
        self.value = value

    @abstractmethod
    def __repr__(self) -> str:
        pass

    # BlockScript Operators
    def add(self, other: Value) -> Value:
        match type(self), type(other):
            case Integer(), Integer():
                return Integer(self.value + other.value)


class Integer(Value):
    def __init__(self, value: int) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"Integer({self.value})"


class Float(Value):
    def __init__(self, value: float) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"Float({self.value})"


class String(Value):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"String({self.value})"


class Boolean(Value):
    def __init__(self, value: bool) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"Boolean({self.value})"


class Null(Value):
    def __init__(self) -> None:
        super().__init__(None)

    def __repr__(self) -> str:
        return "Null()"


class Array(Value):
    def __init__(self, value: list[Value]) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"Array({self.value})"


class Dict(Value):
    def __init__(self, value: dict[str, Value]) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"Dict({self.value})"
