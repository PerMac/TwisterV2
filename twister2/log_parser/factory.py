from __future__ import annotations

from typing import Type

from twister2.log_parser.harness_log_parser import HarnessLogParser


class LogParserFactory:
    _parsers: dict[str, Type[HarnessLogParser]] = {}

    @classmethod
    def register_device_class(cls, name: str, klass: Type[HarnessLogParser]) -> None:
        if name not in cls._parsers:
            cls._parsers[name] = klass

    @classmethod
    def get_parser(cls, name: str) -> Type[HarnessLogParser]:
        return cls._parsers[name]


LogParserFactory.register_device_class('harness', HarnessLogParser)
