from .base import SpanError
from BlockScript.common import Span


class InterpreterError(SpanError):
    pass


class VariableNameError(InterpreterError):
    pass


class InvalidOperatorError(InterpreterError):
    def __init__(self, span: Span, msg: str, left: str, op: str, right: str):
        self.left = left
        self.op = op
        self.right = right
        super().__init__(span, msg)
