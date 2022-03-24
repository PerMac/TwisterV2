"""
Simple class to generate test plan report in CSV format
"""
import csv
import logging
import os

from twister2.report.base_report_writer import BaseWritter

logger = logging.getLogger(__name__)


class CsvTestPlan(BaseWritter):
    """Create test plan report as CSV file."""

    def __init__(self, filename: str, delimiter: str = ';', quotechar: str = '"'):
        """
        :param filename: output file name
        :param: delimiter:
        :param quotechar:
        """
        self.filename = self._normalize_logfile_path(filename)
        self.delimiter = delimiter
        self.quotechar = quotechar

    def write(self, data: list) -> None:
        if not data:
            logger.warning('No data to generate test plan')
            return

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'w', encoding='UTF-8', newline='') as fd:
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(
                fd,
                fieldnames=fieldnames,
                delimiter=self.delimiter,
                quotechar=self.quotechar,
                quoting=csv.QUOTE_MINIMAL
            )
            writer.writeheader()
            writer.writerows(data)
