"""
kafka_consumer.py
-----------------
High Performance Kafka Consumer
Compatible with kafka-python 2.2.15
"""

import json
import time

from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError

from config import (
    BOOTSTRAP_SERVER,
    INPUT_TOPIC,
    AUTO_OFFSET_RESET,
    ENABLE_AUTO_COMMIT,
    MAX_POLL_RECORDS,
    POLL_TIMEOUT_MS,
    SESSION_TIMEOUT_MS,
    HEARTBEAT_INTERVAL_MS,
)

from logger import IDSLogger


class PreprocessingConsumer:

    def __init__(self):

        self.logger = IDSLogger().get_logger()

        self.running = True

        self.consumer = KafkaConsumer(

            bootstrap_servers=BOOTSTRAP_SERVER,

            enable_auto_commit=ENABLE_AUTO_COMMIT,

            auto_offset_reset=AUTO_OFFSET_RESET,

            max_poll_records=MAX_POLL_RECORDS,

            session_timeout_ms=SESSION_TIMEOUT_MS,

            heartbeat_interval_ms=HEARTBEAT_INTERVAL_MS,

            consumer_timeout_ms=1000,

            request_timeout_ms=120000,

            reconnect_backoff_ms=1000,

            reconnect_backoff_max_ms=10000,

            value_deserializer=lambda x: json.loads(
                x.decode("utf-8")
            )

        )

        # ==========================================================
        # Manual Partition Assignment
        # ==========================================================

        tp = TopicPartition(INPUT_TOPIC, 0)

        self.consumer.assign([tp])

        self.consumer.seek_to_beginning(tp)

        self.logger.info("=" * 70)
        self.logger.info(f"Connected to Kafka Topic : {INPUT_TOPIC}")
        self.logger.info("Consumer Started Successfully")
        self.logger.info("=" * 70)

    # ==========================================================
    # Consume
    # ==========================================================

    def consume(self):

        while self.running:

            try:

                batches = self.consumer.poll(

                    timeout_ms=POLL_TIMEOUT_MS,

                    max_records=MAX_POLL_RECORDS

                )

                if not batches:
                    continue

                for _, messages in batches.items():

                    for message in messages:

                        yield message.value

            except KafkaError as e:

                self.logger.error(
                    f"Kafka Consumer Error : {e}"
                )

                time.sleep(2)

            except Exception as e:

                self.logger.exception(
                    f"Unexpected Consumer Error : {e}"
                )

                time.sleep(2)

    # ==========================================================
    # Close
    # ==========================================================

    def close(self):

        self.running = False

        try:

            self.consumer.close()

            self.logger.info(
                "Kafka Consumer Closed Successfully."
            )

        except Exception as e:

            self.logger.exception(
                f"Consumer Close Error : {e}"
            )