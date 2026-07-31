# 🛡️ IR-IDS
## A NETWORK BASED INTRUSION DETECTION SYSTEM BASED ON CAUSAL FEATURE AND EXPLAINABLE MODEL OPTIMIZATION 
[USING APACHE KAFKA AND DOCKER]


<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Kafka](https://img.shields.io/badge/Apache-Kafka-orange)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

# 📖 Overview

IR-IDS is a distributed, Kafka-based Intrusion Detection System designed to detect cyber attacks in real time using machine learning.

Unlike conventional IDS solutions, IR-IDS follows a microservice architecture where each stage of the pipeline communicates through Apache Kafka topics.

The project supports:

- Real-time packet ingestion
- Data preprocessing
- Feature engineering
- Machine learning classification
- Unknown attack detection
- Threat intelligence integration
- Adaptive learning
- Alert generation

---

# 🚀 Key Features

- Apache Kafka Streaming Pipeline
- Distributed Microservice Architecture
- High Throughput Processing
- Real-Time Detection
- Feature Selection
- Machine Learning Classification
- Unknown Attack Detection
- Adaptive Learning
- Alert Dashboard
- Docker Support

---

# 🏗️ System Architecture

> Add the architecture image below.

<p align="center">

<img src="docs/architecture.png" width="95%">

</p>

The system is divided into four major pipelines:

- Real-Time Detection Pipeline
- Offline Training Pipeline
- Adaptive Learning Pipeline
- Alert Pipeline

---

# 📂 Repository Structure

```text
IR-IDS-PROJECT-

├── docker/
│   └── docker-compose.yml
│
├── kafka/
│
├── services/
│
│   ├── ingestion/
│   │
│   ├── preprocessing/
│   │
│   ├── feature_selection/
│   │
│   ├── classification/
│   │
│   └── alert_service/
│
├── datasets/
│
├── models/
│
├── docs/
│   └── architecture.png
│
├── README.md
└── .gitignore
```

---

# ⚙️ Technology Stack

## Backend

- Python 3.13

## Streaming

- Apache Kafka

## Containerization

- Docker
- Docker Compose

## Data Processing

- Pandas
- NumPy

## Machine Learning

- Scikit-learn
- XGBoost
- LightGBM
- CatBoost

## Deep Learning

- TensorFlow
- Keras

## Version Control

- Git
- GitHub

---

# 🔄 System Workflow

```text
CSV Dataset

↓

Kafka Producer

↓

raw-traffic

↓

Preprocessing Service

↓

clean-traffic

↓

Feature Selection

↓

selected-features

↓

Classification Service

↓

classification-results

↓

Alert Service

↓

alerts
```

---

# 📡 Kafka Topics

| Topic | Purpose |
|---------|----------|
| raw-traffic | Raw network traffic |
| clean-traffic | Cleaned traffic |
| selected-features | Selected ML features |
| classification-results | Prediction output |
| alerts | Security alerts |

---

# 🧩 Microservices

## Ingestion Service

Responsibilities

- Read dataset
- Publish records to Kafka
- High-speed producer

---

## Preprocessing Service

Responsibilities

- Validate records
- Clean data
- Normalize values
- Publish clean records

---

## Feature Selection Service

Responsibilities

- Remove irrelevant features
- Select optimal attributes
- Publish selected features

---

## Classification Service

Responsibilities

- Load trained ML model
- Predict attack type
- Publish predictions

---

## Alert Service

Responsibilities

- Generate alerts
- Store incidents
- Notify dashboard

---

# 🐳 Docker Setup

Start Kafka

```bash
cd docker

docker compose up -d
```

Verify

```bash
docker ps
```

Kafka UI

```
http://localhost:8080
```

Broker

```
localhost:9092
```

---

# 💻 Installation

Clone Repository

```bash
git clone https://github.com/<username>/IR-IDS-PROJECT-.git

cd IR-IDS-PROJECT-
```

Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

Install Dependencies

```bash
pip install -r services/preprocessing/requirements.txt
```

---

# ▶️ Running the Project

### 1. Start Kafka

```bash
docker compose up -d
```

### 2. Run Ingestion

```bash
cd services/ingestion

python csv_reader.py
```

### 3. Run Preprocessing

```bash
cd services/preprocessing

python service.py
```

Future Services

```text
Feature Selection

↓

Classification

↓

Alert Service
```

---

# 📊 Dataset

Current Dataset

- Historical IDS Dataset

Future Support

- CICIDS2017
- CICIDS2018
- CSE-CIC-IDS2018
- UNSW-NB15
- TON-IoT

---

# 🧠 Machine Learning Pipeline

Feature Engineering

↓

Feature Selection

↓

Train/Test Split

↓

Model Training

↓

Evaluation

↓

Model Registry

↓

Real-Time Prediction

---

# 📈 Project Roadmap

- [x] Kafka Infrastructure
- [x] Docker Setup
- [x] Data Ingestion
- [x] Data Preprocessing
- [ ] Feature Selection
- [ ] Model Training
- [ ] Classification Service
- [ ] Alert Service
- [ ] Dashboard
- [ ] Adaptive Learning

---

# 👨‍💻 Contributors

| Name | Responsibility |
|--------|---------------|
| Revaan J R | Team Lead, Kafka Integration, Backend |
| Member 2 | Feature Engineering |
| Member 3 | Machine Learning |
| Member 4 | Dashboard & Alert Service |

---

# 📜 License

This project is developed as part of a Final Year Artificial Intelligence & Data Science Project.

MIT License.

---

⭐ If you find this project useful, consider giving it a star.
