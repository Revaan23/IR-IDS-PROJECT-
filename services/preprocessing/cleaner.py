"""
cleaner.py
----------
High Performance Data Cleaner for IR-IDS
"""

import math
from typing import Dict, Any

from config import (
    REPLACE_NULL_WITH,
    REPLACE_INFINITY_WITH,
    TRIM_WHITESPACE,
    NORMALIZE_COLUMN_NAMES,
    NORMALIZE_LABELS,
)

from schema import (
    COLUMN_MAPPING,
    NUMERIC_COLUMNS,
    LABEL_MAPPING,
)


class DataCleaner:

    def __init__(self):

        self.cleaned_records = 0

        # Convert to set for O(1) lookups
        self.numeric_columns = set(NUMERIC_COLUMNS)

    # ==========================================================
    # Complete Cleaning Pipeline (Single Pass)
    # ==========================================================

    def clean_record(self, record: Dict[str, Any]) -> Dict[str, Any]:

        cleaned = {}

        for key, value in record.items():

            # -------------------------------
            # Normalize column names
            # -------------------------------

            if NORMALIZE_COLUMN_NAMES:
                key = COLUMN_MAPPING.get(key, key)

            # -------------------------------
            # Handle NULL
            # -------------------------------

            if value is None:
                value = REPLACE_NULL_WITH

            # -------------------------------
            # Trim strings
            # -------------------------------

            elif TRIM_WHITESPACE and isinstance(value, str):
                value = value.strip()

            # -------------------------------
            # Numeric conversion
            # -------------------------------

            if key in self.numeric_columns:

                try:

                    value = float(value)

                    if math.isnan(value):
                        value = REPLACE_NULL_WITH

                    elif math.isinf(value):
                        value = REPLACE_INFINITY_WITH

                except Exception:

                    value = REPLACE_NULL_WITH

            cleaned[key] = value

        # -------------------------------
        # Normalize Label
        # -------------------------------

        if NORMALIZE_LABELS:

            if "label" in cleaned:

                label = str(cleaned["label"]).strip()

                cleaned["label"] = LABEL_MAPPING.get(
                    label,
                    label.upper()
                )

            elif "Label" in cleaned:

                label = str(cleaned["Label"]).strip()

                cleaned["Label"] = LABEL_MAPPING.get(
                    label,
                    label.upper()
                )

        self.cleaned_records += 1

        return cleaned

    # ==========================================================

    def get_statistics(self):

        return {
            "cleaned_records": self.cleaned_records
        }

    # ==========================================================

    def reset_statistics(self):

        self.cleaned_records = 0