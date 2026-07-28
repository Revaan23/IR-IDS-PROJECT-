"""
logger.py
---------
Enterprise Logging Utility
"""

import logging
from logging.handlers import RotatingFileHandler

from config import (
    LOG_FOLDER,
    LOG_FILE,
    LOG_LEVEL
)


class IDSLogger:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._initialize()

        return cls._instance

    def _initialize(self):

        LOG_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        self.logger = logging.getLogger("IR-IDS")

        self.logger.setLevel(getattr(logging, LOG_LEVEL))

        # Avoid duplicate handlers
        if self.logger.handlers:
            return

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)-8s | %(message)s",

            "%Y-%m-%d %H:%M:%S"

        )

        # =====================================
        # Console Logger
        # =====================================

        console = logging.StreamHandler()

        console.setFormatter(formatter)

        self.logger.addHandler(console)

        # =====================================
        # Rotating File Logger
        # =====================================

        file_handler = RotatingFileHandler(

            LOG_FILE,

            maxBytes=5 * 1024 * 1024,

            backupCount=5,

            encoding="utf-8"

        )

        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def get_logger(self):

        return self.logger