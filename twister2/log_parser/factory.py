from __future__ import annotations

import logging
from typing import Type

from twister2.log_parser.harness_log_parser import HarnessLogParser

logger = logging.getLogger(__name__)


class LogParserFactory:
    _parsers: dict[str, Type[HarnessLogParser]] = {}

    @classmethod
    def register_device_class(cls, name: str, klass: Type[HarnessLogParser]) -> None:
        if name not in cls._parsers:
            cls._parsers[name] = klass

    @classmethod
    def get_parser(cls, name: str) -> Type[HarnessLogParser]:
        try:
            return cls._parsers[name]
        except KeyError as e:
            logger.exception('There is not parser with name: %s', name)
            raise KeyError(f'Parser "{name}" does not exist') from e


LogParserFactory.register_device_class('harness', HarnessLogParser)
