"""
service.py
----------
IR-IDS Preprocessing Service
Optimized for kafka-python
"""

import time

from kafka_consumer import PreprocessingConsumer
from kafka_producer import PreprocessingProducer
from validator import RecordValidator
from cleaner import DataCleaner
from logger import IDSLogger
from config import PRINT_STATS_EVERY


class PreprocessingService:

    def __init__(self):

        self.logger = IDSLogger().get_logger()

        self.consumer = PreprocessingConsumer()
        self.producer = PreprocessingProducer()

        self.validator = RecordValidator()
        self.cleaner = DataCleaner()

        self.processed_records = 0
        self.start_time = time.time()

    # ==========================================================
    # Process One Record
    # ==========================================================

    def process_record(self, record):

        valid, _ = self.validator.validate(record)

        if not valid:
            return

        cleaned = self.cleaner.clean_record(record)

        self.producer.send(cleaned)

        self.processed_records += 1

        # Flush periodically to reduce producer queue buildup
        if self.processed_records % PRINT_STATS_EVERY == 0:

            self.producer.flush()

            self.print_statistics()

    # ==========================================================
    # Print Statistics
    # ==========================================================

    def print_statistics(self):

        validator_stats = self.validator.get_statistics()
        cleaner_stats = self.cleaner.get_statistics()

        elapsed = max(time.time() - self.start_time, 1)

        speed = self.processed_records / elapsed

        self.logger.info("=" * 70)
        self.logger.info("PREPROCESSING STATISTICS")
        self.logger.info("=" * 70)
        self.logger.info(
            f"Processed Records : {self.processed_records:,}"
        )
        self.logger.info(
            f"Processing Speed  : {speed:.2f} records/sec"
        )
        self.logger.info(
            f"Valid Records     : {validator_stats['valid_records']:,}"
        )
        self.logger.info(
            f"Invalid Records   : {validator_stats['invalid_records']:,}"
        )
        self.logger.info(
            f"Cleaned Records   : {cleaner_stats['cleaned_records']:,}"
        )
        self.logger.info("=" * 70)

    # ==========================================================
    # Run Service
    # ==========================================================

    def run(self):

        self.logger.info("=" * 70)
        self.logger.info("IR-IDS PREPROCESSING SERVICE STARTED")
        self.logger.info("=" * 70)

        try:

            for record in self.consumer.consume():

                self.process_record(record)

        except KeyboardInterrupt:

            self.logger.info("Keyboard Interrupt Received")

        except Exception as e:

            self.logger.exception(
                f"Unexpected Error : {e}"
            )

        finally:

            self.shutdown()

    # ==========================================================
    # Shutdown
    # ==========================================================

    def shutdown(self):

        self.logger.info("=" * 70)
        self.logger.info("Stopping Service...")
        self.logger.info("=" * 70)

        # Flush pending producer messages
        try:

            self.producer.flush()

        except Exception as e:

            self.logger.exception(
                f"Producer Flush Error : {e}"
            )

        # Close Consumer
        try:

            self.consumer.close()

        except Exception as e:

            self.logger.exception(
                f"Consumer Close Error : {e}"
            )

        # Close Producer
        try:

            self.producer.close()

        except Exception as e:

            self.logger.exception(
                f"Producer Close Error : {e}"
            )

        elapsed = max(time.time() - self.start_time, 1)

        self.logger.info("=" * 70)
        self.logger.info("FINAL REPORT")
        self.logger.info("=" * 70)
        self.logger.info(
            f"Processed Records : {self.processed_records:,}"
        )
        self.logger.info(
            f"Total Time        : {elapsed:.2f} sec"
        )
        self.logger.info(
            f"Average Speed     : {self.processed_records / elapsed:.2f} records/sec"
        )
        self.logger.info("=" * 70)

        self.logger.info("Service Shutdown Completed")


if __name__ == "__main__":

    service = PreprocessingService()

    service.run()