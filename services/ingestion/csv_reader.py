"""
csv_reader.py
-------------
Enterprise CSV Reader

Features
--------
✓ Memory Efficient
✓ Chunk Streaming
✓ Resume from Checkpoint
✓ Progress Display
✓ Exception Handling
✓ Fast Iteration
"""

from pathlib import Path
import pandas as pd

from config import (
    CHUNK_SIZE,
    CSV_ENCODING
)

from checkpoint import CheckpointManager
from logger import IDSLogger


class CSVReader:

    def __init__(self, dataset_folder):

        self.dataset_folder = Path(dataset_folder)

        self.logger = IDSLogger().get_logger()

        self.checkpoint = CheckpointManager()

    # ==========================================================
    # Locate CSV Files
    # ==========================================================

    def get_csv_files(self):

        csv_files = sorted(
            self.dataset_folder.rglob("*.csv")
        )

        if not csv_files:

            raise FileNotFoundError(

                f"No CSV files found in\n{self.dataset_folder}"

            )

        return csv_files

    # ==========================================================
    # Stream Records
    # ==========================================================

    def read_rows(self):

        csv_files = self.get_csv_files()

        checkpoint = self.checkpoint.load()

        resume_file = None
        resume_chunk = 0

        if checkpoint:

            resume_file = checkpoint.get("file")

            resume_chunk = checkpoint.get("chunk", 0)

            self.logger.info(

                "Checkpoint Found"

            )

            self.logger.info(

                f"Resuming File : {resume_file}"

            )

            self.logger.info(

                f"Resume Chunk  : {resume_chunk}"

            )

        resume_mode = resume_file is not None

        # ======================================================

        for csv_file in csv_files:

            file_name = csv_file.name

            if resume_mode:

                if file_name != resume_file:

                    continue

                resume_mode = False

            print(f"\nReading : {file_name}")

            self.logger.info(

                f"Reading {file_name}"

            )

            try:

                chunk_iterator = pd.read_csv(

                    csv_file,

                    chunksize=CHUNK_SIZE,

                    low_memory=False,

                    encoding=CSV_ENCODING

                )

            except Exception as e:

                self.logger.error(str(e))

                continue

            for chunk_number, chunk in enumerate(chunk_iterator):

                if (

                    file_name == resume_file and

                    chunk_number < resume_chunk

                ):

                    continue

                chunk.fillna(

                    value=None,

                    inplace=True

                )

                # ----------------------------------------------

                # Faster than to_dict(orient="records")

                # ----------------------------------------------

                columns = chunk.columns.tolist()

                values = chunk.values.tolist()

                for row_number, row_values in enumerate(values):

                    row = dict(

                        zip(

                            columns,

                            row_values

                        )

                    )

                    yield (

                        file_name,

                        chunk_number,

                        row_number,

                        row

                    )

        self.logger.info(

            "CSV Streaming Finished"

        )