"""
config.py
---------
Enterprise Configuration for the IR-IDS Ingestion Service
"""

from pathlib import Path

# =============================================================================
# Project Paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# =============================================================================
# Dataset Configuration
# =============================================================================

# Development Dataset
DATASET_FOLDER = PROJECT_ROOT / "datasets" / "raw" / "CSE-CIC-IDS2018-50K"

# Production Dataset (Uncomment when required)
# DATASET_FOLDER = PROJECT_ROOT / "datasets" / "raw" / "CSE-CIC-IDS2018"

# =============================================================================
# Kafka Configuration
# =============================================================================

BOOTSTRAP_SERVER = "localhost:9092"

TOPIC_NAME = "raw-traffic"

CLIENT_ID = "ir-ids-producer"

# =============================================================================
# Kafka Producer Performance
# =============================================================================

# Number of messages accumulated before sending
BATCH_SIZE = 131072          # 128 KB

# Wait up to 50ms to build larger batches
LINGER_MS = 50

# Kafka Producer Buffer (64 MB)
BUFFER_MEMORY = 67108864

# Compression (fast + smaller network traffic)
COMPRESSION_TYPE = "gzip"

# Number of retries
MAX_RETRIES = 3

# Retry delay
RETRY_DELAY = 2

# Fast acknowledgements
ACKS = 1

# Maximum in-flight requests
MAX_IN_FLIGHT = 5

# =============================================================================
# CSV Reader
# =============================================================================

# Increase for better throughput
CHUNK_SIZE = 20000

CSV_ENCODING = "utf-8"

# =============================================================================
# Checkpoint
# =============================================================================

CHECKPOINT_FOLDER = Path(__file__).parent / "checkpoints"

CHECKPOINT_FILE = CHECKPOINT_FOLDER / "checkpoint.json"

# Save checkpoint every 20k records
SAVE_CHECKPOINT_EVERY = 20000

# =============================================================================
# Logging
# =============================================================================

LOG_FOLDER = Path(__file__).parent / "logs"

LOG_FILE = LOG_FOLDER / "ingestion.log"

LOG_LEVEL = "INFO"

# =============================================================================
# Progress
# =============================================================================

SHOW_PROGRESS = True

SHOW_RECORD_RATE = True

# =============================================================================
# Statistics
# =============================================================================

PRINT_SUMMARY = True