from .base import SpanError


class ParserError(SpanError):
    pass


class UnexpectedEOF(ParserError):
    def __init__(self, span, msg):
        super().__init__(span, msg)


class UnexpectedToken(ParserError):
    def __init__(self, span, msg, token):
        self.token = token
        super().__init__(span, msg)
