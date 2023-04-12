from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Location:
    def __init__(self, filename: str, line: int, column: int) -> None:
        self.filename = filename
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"{self.filename}:{self.line}:{self.column}"


@dataclass
class Span:
    def __init__(self, start: Location, end: Location) -> None:
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"{self.start} - {self.end}"

    def extend(self, other: Span) -> Span:
        return Span(self.start, other.end)
