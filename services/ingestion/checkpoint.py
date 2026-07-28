"""
checkpoint.py
-------------
Enterprise Checkpoint Manager

Features
--------
✓ Automatic checkpoint creation
✓ Safe loading
✓ Atomic writes
✓ Corruption recovery
✓ Reset support
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime

from config import (
    CHECKPOINT_FOLDER,
    CHECKPOINT_FILE
)


class CheckpointManager:

    def __init__(self):

        CHECKPOINT_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        if not CHECKPOINT_FILE.exists():
            self.reset()

    # ==========================================================
    # Save Checkpoint
    # ==========================================================

    def save(
        self,
        file_name: str,
        chunk: int,
        records_sent: int
    ):

        checkpoint = {

            "file": file_name,

            "chunk": chunk,

            "records_sent": records_sent,

            "timestamp": datetime.now().isoformat()

        }

        temp_file = CHECKPOINT_FILE.with_suffix(".tmp")

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                checkpoint,
                f,
                indent=4
            )

        temp_file.replace(CHECKPOINT_FILE)

    # ==========================================================
    # Load Checkpoint
    # ==========================================================

    def load(self):

        if not CHECKPOINT_FILE.exists():
            return None

        try:

            with open(
                CHECKPOINT_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                checkpoint = json.load(f)

            if not checkpoint:
                return None

            return checkpoint

        except Exception:

            return None

    # ==========================================================
    # Reset Checkpoint
    # ==========================================================

    def reset(self):

        with open(
            CHECKPOINT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {},
                f,
                indent=4
            )

    # ==========================================================
    # Delete Checkpoint
    # ==========================================================

    def delete(self):

        if CHECKPOINT_FILE.exists():
            CHECKPOINT_FILE.unlink()

    # ==========================================================
    # Exists
    # ==========================================================

    def exists(self):

        return CHECKPOINT_FILE.exists()