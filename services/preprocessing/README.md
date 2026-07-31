# IR-IDS Preprocessing Service

## Overview

The Preprocessing Service is the second microservice in the IR-IDS pipeline.

It consumes raw network traffic records from Kafka, validates them, cleans the data, and publishes standardized records for feature selection.

---

## Pipeline

CSV Ingestion Service
        │
        ▼
raw-traffic
        │
        ▼
Preprocessing Service
        │
        ▼
clean-traffic

---

## Folder Structure

preprocessing/

├── config.py
├── logger.py
├── schema.py
├── validator.py
├── cleaner.py
├── kafka_consumer.py
├── kafka_producer.py
├── service.py
├── requirements.txt
├── README.md
├── logs/
└── tests/

---

## Responsibilities

- Consume records from Kafka
- Validate records
- Normalize column names
- Replace null values
- Replace NaN/Infinity
- Convert numeric fields
- Normalize labels
- Publish cleaned records

---

## Input Topic

raw-traffic

---

## Output Topic

clean-traffic

---

## Run

Install dependencies

pip install -r requirements.txt

Start Kafka

docker compose up -d

Run the service

python service.py

---

## Logs

All logs are written to

logs/preprocessing.log

---

## Next Service

Feature Selection Service

Input Topic:

clean-traffic

Output Topic:

selected-features