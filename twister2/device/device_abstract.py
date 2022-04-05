from __future__ import annotations

import abc
import logging
from pathlib import Path
from threading import Lock

logger = logging.getLogger(__name__)


class DeviceAbstract(abc.ABC):

    def __init__(self):
        self.id: str = ''
        self.serial: str = ''
        self.platform: str = ''
        self.lock: Lock = Lock()
        self.log_file: str | Path = 'device.log'

    def __repr__(self):
        return f'{self.__class__.__name__}(id="{self.id}")'

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    @abc.abstractmethod
    def flash(self, build_dir: str | Path, timeout: float = 60.0) -> None:
        """
        Flash and run code on a device.

        :param build_dir: build directory
        :param timeout: time out in seconds
        """
