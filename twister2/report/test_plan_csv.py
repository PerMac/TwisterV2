import csv
import os


class CsvTestPlan:

    def __init__(self, filename: str):
        self.filename = filename
        self.delimiter = ','
        self.quotechar = '"'

    def build(self, data: list) -> list:
        return data

    def write(self, data: list) -> None:
        if not data:
            return

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'w', newline='') as fd:
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
            