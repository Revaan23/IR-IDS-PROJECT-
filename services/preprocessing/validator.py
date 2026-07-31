"""
validator.py
------------
High Performance Record Validator
"""

from typing import Dict, Any

from schema import REQUIRED_COLUMNS


class RecordValidator:

    def __init__(self):

        self.valid_records = 0
        self.invalid_records = 0

    # ==========================================================

    def validate(self, record: Dict[str, Any]):

        if not record or not isinstance(record, dict):

            self.invalid_records += 1

            return False, "Empty Record"

        for column in REQUIRED_COLUMNS:

            value = record.get(column)

            if value is None:

                self.invalid_records += 1

                return False, f"Missing or None: {column}"

            if isinstance(value, str) and not value.strip():

                self.invalid_records += 1

                return False, f"Empty: {column}"

        self.valid_records += 1

        return True, "Valid"

    # ==========================================================

    def get_statistics(self):

        return {
            "valid_records": self.valid_records,
            "invalid_records": self.invalid_records,
        }

    # ==========================================================

    def reset_statistics(self):

        self.valid_records = 0
        self.invalid_records = 0