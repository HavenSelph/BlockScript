from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
from BlockScript.Errors.interpreter import *


def op_error(span: Span, left: Value, op: str, right: Value) -> InvalidOperatorError:
    return InvalidOperatorError(span, f"'+' not defined for types {left} and {right}", str(type(left)), op, str(type(right)))


class ValueTypes(Enum):
    Integer = auto()
    Float = auto()
    String = auto()

    Null = auto()


class Value(ABC):
    def __init__(self, value, kind: ValueTypes) -> None:
        self.value = value
        self.kind = kind

    @abstractmethod
    def __repr__(self) -> str:
        pass

    # BlockScript Operators
    def add(self, other: Value, span: Span) -> Value:
        match self.kind, other.kind:
            case ValueTypes.Integer, ValueTypes.Integer:
                return Integer(self.value + other.value)
            case ValueTypes.Integer, ValueTypes.Float:
                return Float(self.value + other.value)
            case ValueTypes.Float, ValueTypes.Integer:
                return Float(self.value + other.value)
            case ValueTypes.Float, ValueTypes.Float:
                return Float(self.value + other.value)
            case left, right:
                raise op_error(span, self, "+", other)

    def subtract(self, other: Value, span: Span) -> Value:
        match self, other:
            case Integer(), Integer():
                return Integer(self.value - other.value)
            case Integer(), Float():
                return Float(self.value - other.value)
            case Float(), Integer():
                return Float(self.value - other.value)
            case Float(), Float():
                return Float(self.value - other.value)
            case left, right:
                raise op_error(span, self, "-", other)


class Integer(Value):
    def __init__(self, value: int) -> None:
        super().__init__(value, ValueTypes.Integer)

    def __repr__(self) -> str:
        return f"Integer({self.value})"


class Float(Value):
    def __init__(self, value: float) -> None:
        super().__init__(value, ValueTypes.Float)

    def __repr__(self) -> str:
        return f"Float({self.value})"


class Null(Value):
    def __init__(self) -> None:
        super().__init__(None, ValueTypes.Null)

    def __repr__(self) -> str:
        return "Null()"
