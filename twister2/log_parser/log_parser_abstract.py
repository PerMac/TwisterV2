from __future__ import annotations

import abc
from dataclasses import dataclass, asdict
from typing import Generator, Iterator


class LogParserAbstract(abc.ABC):

    def __init__(self, stream: Iterator[str]):
        self.stream = stream
        self.state: str = 'PASSED'  # overall status for execution
        self.messages: list[str] = []

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    @abc.abstractmethod
    def parse(self) -> Generator[SubTestResult, None, None] | None:
        pass


@dataclass
class SubTestResult:
    """Store result for single C tests."""
    testname: str
    result: str
    duration: float

    def __post_init__(self):
        if isinstance(self.duration, str):
            self.duration = float(self.duration)

    def asdict(self) -> dict:
        return asdict(self)
