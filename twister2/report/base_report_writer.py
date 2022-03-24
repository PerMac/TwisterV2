import abc
import os


class BaseReportWriter(abc.ABC):

    @staticmethod
    def _normalize_logfile_path(filename: str) -> str:
        filename = os.path.expanduser(os.path.expandvars(filename))
        filename = os.path.normpath(os.path.abspath(filename))
        return filename

    @abc.abstractmethod
    def write(self, data: list) -> None:
        """Save report."""
