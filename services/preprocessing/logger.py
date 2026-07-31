"""
logger.py
----------
Enterprise Logger for the IR-IDS Preprocessing Service.
"""

import logging

from config import (
    LOG_FOLDER,
    LOG_FILE,
    LOG_LEVEL,
    LOG_FORMAT,
    DATE_FORMAT
)


class IDSLogger:

    """
    Enterprise Logger

    Features
    --------
    ✓ Console Logging
    ✓ File Logging
    ✓ Timestamp
    ✓ Log Levels
    ✓ Singleton Logger
    """

    def __init__(self):

        LOG_FOLDER.mkdir(

            parents=True,

            exist_ok=True

        )

        self.logger = logging.getLogger(

            "IR_IDS_PREPROCESSING"

        )

        if self.logger.hasHandlers():

            return

        # ==========================================================
        # Logger Level
        # ==========================================================

        self.logger.setLevel(

            getattr(

                logging,

                LOG_LEVEL

            )

        )

        # ==========================================================
        # Formatter
        # ==========================================================

        formatter = logging.Formatter(

            fmt=LOG_FORMAT,

            datefmt=DATE_FORMAT

        )

        # ==========================================================
        # Console Handler
        # ==========================================================

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(

            formatter

        )

        # ==========================================================
        # File Handler
        # ==========================================================

        file_handler = logging.FileHandler(

            LOG_FILE,

            encoding="utf-8"

        )

        file_handler.setFormatter(

            formatter

        )

        # ==========================================================
        # Add Handlers
        # ==========================================================

        self.logger.addHandler(

            console_handler

        )

        self.logger.addHandler(

            file_handler

        )

    # ==============================================================
    # Return Logger
    # ==============================================================

    def get_logger(self):

        return self.logger