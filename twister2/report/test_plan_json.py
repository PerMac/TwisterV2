import json
import logging
import os

from twister2.report.base_report_writer import BaseWritter

logger = logging.getLogger(__name__)


class JsonTestPlan(BaseWritter):

    def __init__(self, filename: str) -> None:
        self.filename = self._normalize_logfile_path(filename)

    def write(self, data: list) -> None:
        if not data:
            logger.warning('No data to generate test plan')
            return

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'w', encoding='UTF-8') as fd:
            json.dump(data, fd, indent=4)
