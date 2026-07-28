"""
producer.py
-----------
Enterprise IR-IDS Dataset Ingestion Service

Features
--------
✓ Async Kafka Streaming
✓ Checkpoint Resume
✓ Graceful Shutdown
✓ Progress Bar
✓ ETA
✓ Records/sec
✓ Logging
✓ Automatic Retry
"""

import signal
import sys
import time

from tqdm import tqdm

from config import (
    BOOTSTRAP_SERVER,
    TOPIC_NAME,
    DATASET_FOLDER,
    SAVE_CHECKPOINT_EVERY
)

from csv_reader import CSVReader
from kafka_producer import IDSKafkaProducer
from checkpoint import CheckpointManager
from logger import IDSLogger


logger = IDSLogger().get_logger()

checkpoint = CheckpointManager()

producer = None

last_file = None
last_chunk = 0
records_sent = 0

start_time = None


# ==========================================================
# Graceful Shutdown
# ==========================================================

def shutdown_handler(sig, frame):

    global producer
    global last_file
    global last_chunk
    global records_sent

    print()

    logger.info("Ctrl+C Detected")

    print("Saving checkpoint...")

    checkpoint.save(
        file_name=last_file,
        chunk=last_chunk,
        records_sent=records_sent
    )

    logger.info("Checkpoint Saved")

    if producer:

        producer.flush()

        producer.close()

    print("Checkpoint Saved.")
    print("Producer Closed.")
    print("Goodbye.")

    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_handler)


# ==========================================================
# Main
# ==========================================================

def main():

    global producer
    global last_file
    global last_chunk
    global records_sent
    global start_time

    print("=" * 70)
    print("IR-IDS Dataset Ingestion Service")
    print("=" * 70)

    print(f"Dataset : {DATASET_FOLDER}")
    print(f"Kafka   : {BOOTSTRAP_SERVER}")
    print(f"Topic   : {TOPIC_NAME}")
    print()

    logger.info("Starting Ingestion Service")

    start_time = time.time()

    reader = CSVReader(DATASET_FOLDER)

    producer = IDSKafkaProducer(
        BOOTSTRAP_SERVER,
        TOPIC_NAME
    )

    progress = tqdm(
        desc="Streaming Records",
        unit="records"
    )

    try:

        for (
            file_name,
            chunk_number,
            row_number,
            row
        ) in reader.read_rows():

            # Async send
            producer.send(row)

            records_sent += 1

            last_file = file_name
            last_chunk = chunk_number

            progress.update(1)

            # Save checkpoint every N records
            if records_sent % SAVE_CHECKPOINT_EVERY == 0:

                producer.flush()

                checkpoint.save(
                    file_name=file_name,
                    chunk=chunk_number,
                    records_sent=records_sent
                )

                elapsed = time.time() - start_time

                rate = (
                    records_sent / elapsed
                    if elapsed > 0
                    else 0
                )

                logger.info(
                    f"Checkpoint Saved ({records_sent:,} records)"
                )

                logger.info(
                    f"Speed : {rate:.2f} records/sec"
                )
                        # ======================================================
        # End of Streaming
        # ======================================================

        producer.flush()

        checkpoint.reset()

        logger.info(
            "Final Kafka Flush Completed"
        )

    except Exception as e:

        logger.exception(
            f"Unexpected Error : {e}"
        )

        checkpoint.save(

            file_name=last_file,

            chunk=last_chunk,

            records_sent=records_sent

        )

        if producer is not None:

            producer.flush()

            producer.close()

        raise

    finally:

        progress.close()

        if producer is not None:

            producer.close()

    # ======================================================
    # Statistics
    # ======================================================

    elapsed = time.time() - start_time

    speed = (

        records_sent / elapsed

        if elapsed > 0

        else 0

    )

    print()

    print("=" * 70)

    print("INGESTION COMPLETED")

    print("=" * 70)

    print(f"Dataset            : {DATASET_FOLDER}")

    print(f"Records Streamed   : {records_sent:,}")

    print(f"Elapsed Time       : {elapsed:.2f} sec")

    print(f"Average Speed      : {speed:.2f} records/sec")

    print("=" * 70)

    logger.info(

        "========================================"

    )

    logger.info(

        "INGESTION COMPLETED"

    )

    logger.info(

        f"Records : {records_sent:,}"

    )

    logger.info(

        f"Elapsed : {elapsed:.2f} sec"

    )

    logger.info(

        f"Average : {speed:.2f} records/sec"

    )

    logger.info(

        "========================================"

    )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        shutdown_handler(None, None)