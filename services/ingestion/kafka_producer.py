"""
kafka_producer.py
-----------------
High Performance Kafka Producer
Compatible with kafka-python
"""

import json

from kafka import KafkaProducer
from kafka.errors import KafkaError

from config import (
    MAX_RETRIES,
    RETRY_DELAY,
    BATCH_SIZE,
    LINGER_MS,
    COMPRESSION_TYPE,
    ACKS,
    MAX_IN_FLIGHT
)

from logger import IDSLogger


class IDSKafkaProducer:

    def __init__(
        self,
        bootstrap_server: str,
        topic: str
    ):

        self.topic = topic

        self.logger = IDSLogger().get_logger()

        self.messages_sent = 0
        self.failed_messages = 0

        self.logger.info(
            f"Connecting to Kafka ({bootstrap_server})..."
        )

        self.producer = KafkaProducer(

            bootstrap_servers=bootstrap_server,

            value_serializer=lambda message:
            json.dumps(
                message,
                default=str
            ).encode("utf-8"),

            # ==================================================
            # Performance Settings
            # ==================================================

            batch_size=BATCH_SIZE,

            linger_ms=LINGER_MS,

            compression_type=COMPRESSION_TYPE,

            retries=MAX_RETRIES,

            retry_backoff_ms=RETRY_DELAY * 1000,

            acks=ACKS,

            max_in_flight_requests_per_connection=MAX_IN_FLIGHT,

            max_request_size=10 * 1024 * 1024,

            max_block_ms=60000

        )

        print(f"✅ Connected to Kafka Broker ({bootstrap_server})")

        self.logger.info("Kafka Producer Connected.")

    # ======================================================
    # Success Callback
    # ======================================================

    def _on_success(self, metadata):

        self.messages_sent += 1

    # ======================================================
    # Error Callback
    # ======================================================

    def _on_error(self, exception):

        self.failed_messages += 1

        self.logger.error(
            f"Kafka Error : {exception}"
        )

    # ======================================================
    # Send Message (ASYNC)
    # ======================================================

    def send(
        self,
        message: dict
    ):

        try:

            future = self.producer.send(
                self.topic,
                value=message
            )

            future.add_callback(self._on_success)

            future.add_errback(self._on_error)

            return True

        except KafkaError as e:

            self.failed_messages += 1

            self.logger.error(str(e))

            return False

    # ======================================================
    # Flush Producer
    # ======================================================

    def flush(self):

        self.producer.flush()

    # ======================================================
    # Statistics
    # ======================================================

    def statistics(self):

        return {
            "messages_sent": self.messages_sent,
            "failed_messages": self.failed_messages
        }

    # ======================================================
    # Close Producer
    # ======================================================

    def close(self):

        try:

            self.producer.flush()

            self.producer.close()

            stats = self.statistics()

            self.logger.info(
                f"Producer Closed | Sent: {stats['messages_sent']:,} | Failed: {stats['failed_messages']:,}"
            )

        except Exception as e:

            self.logger.error(
                f"Close Error : {e}"
            )