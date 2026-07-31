"""
kafka_producer.py
-----------------
Enterprise Kafka Producer
Compatible with kafka-python 2.2.15
"""

import json

from kafka import KafkaProducer
from kafka.errors import KafkaError

from config import (
    BOOTSTRAP_SERVER,
    OUTPUT_TOPIC,
    CLIENT_ID,
    ACKS,
    MAX_RETRIES,
    COMPRESSION_TYPE,
    BATCH_SIZE,
    LINGER_MS,
    MAX_IN_FLIGHT,
    BUFFER_MEMORY,
    REQUEST_TIMEOUT_MS,
    DELIVERY_TIMEOUT_MS,
    MAX_BLOCK_MS,
    RETRY_BACKOFF_MS,
    PRINT_STATS_EVERY,
)

from logger import IDSLogger


class PreprocessingProducer:

    def __init__(self):

        self.logger = IDSLogger().get_logger()

        self.sent_records = 0
        self.success_records = 0
        self.failed_records = 0

        producer_config = {

            "bootstrap_servers": BOOTSTRAP_SERVER,

            "client_id": CLIENT_ID,

            "acks": ACKS,

            "retries": MAX_RETRIES,

            "retry_backoff_ms": RETRY_BACKOFF_MS,

            "batch_size": BATCH_SIZE,

            "linger_ms": LINGER_MS,

            "buffer_memory": BUFFER_MEMORY,

            "request_timeout_ms": REQUEST_TIMEOUT_MS,

            "delivery_timeout_ms": DELIVERY_TIMEOUT_MS,

            "max_block_ms": MAX_BLOCK_MS,

            "max_in_flight_requests_per_connection": MAX_IN_FLIGHT,

            "value_serializer": lambda x: json.dumps(x).encode("utf-8"),
        }

        if COMPRESSION_TYPE:
            producer_config["compression_type"] = COMPRESSION_TYPE

        self.producer = KafkaProducer(**producer_config)

        self.logger.info("=" * 70)
        self.logger.info(f"Connected to Kafka Topic : {OUTPUT_TOPIC}")
        self.logger.info("Kafka Producer Started Successfully")
        self.logger.info("=" * 70)

    # ==========================================================
    # Send
    # ==========================================================

    def send(self, record):

        try:

            future = self.producer.send(
                OUTPUT_TOPIC,
                value=record
            )

            future.add_callback(self._delivery_success)
            future.add_errback(self._delivery_error)

            self.sent_records += 1

            # Flush periodically
            if self.sent_records % PRINT_STATS_EVERY == 0:

                self.producer.flush(timeout=30)

                self.logger.info(
                    f"Queued Records : {self.sent_records:,}"
                )

        except Exception as e:

            self.failed_records += 1

            self.logger.exception(
                f"Producer Error : {e}"
            )

    # ==========================================================
    # Success Callback
    # ==========================================================

    def _delivery_success(self, metadata):

        self.success_records += 1

    # ==========================================================
    # Error Callback
    # ==========================================================

    def _delivery_error(self, exc):

        self.failed_records += 1

        self.logger.error(
            f"Kafka Delivery Failed : {exc}"
        )

    # ==========================================================
    # Flush
    # ==========================================================

    def flush(self):

        try:

            self.producer.flush(timeout=30)

        except KafkaError as e:

            self.logger.exception(
                f"Flush Error : {e}"
            )

    # ==========================================================
    # Close
    # ==========================================================

    def close(self):

        try:

            self.flush()

        finally:

            self.producer.close(timeout=30)

        self.logger.info("=" * 70)
        self.logger.info("PRODUCER SUMMARY")
        self.logger.info("=" * 70)
        self.logger.info(f"Queued Records     : {self.sent_records:,}")
        self.logger.info(f"Delivered Records  : {self.success_records:,}")
        self.logger.info(f"Failed Records     : {self.failed_records:,}")
        self.logger.info("=" * 70)