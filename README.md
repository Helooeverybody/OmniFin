# 🏦 OmniFin: Autonomous Financial Intelligence Platform


![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Spark](https://img.shields.io/badge/Apache_Spark-Streaming-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![MLOps](https://img.shields.io/badge/MLOps-End_to_End-green?style=for-the-badge)
![GenAI](https://img.shields.io/badge/GenAI-RAG_Agent-purple?style=for-the-badge)

> **A Unified Data Lakehouse & MLOps Platform combining Quantitative Market Data with Qualitative News Sentiment to generate Explainable Investment Strategies.**

---

## 📖 Executive Summary

**OmniFin** is an enterprise-grade financial data platform designed to mimic the architecture of modern Fintech unicorns. It solves the challenge of **Multimodal Financial Analysis** by ingesting real-time stock ticks (Quantitative) and unstructured financial news (Qualitative) into a unified **Lakehouse**.

Unlike traditional black-box models, OmniFin utilizes an **Agentic RAG (Retrieval-Augmented Generation)** approach, where a Large Language Model (Llama 3) acts as a portfolio manager, synthesizing technical indicators from the Feature Store with news sentiment from the Vector Database to provide **explainable trading signals** compliant with financial auditing standards.

---

## 🏗️ System Architecture

The platform follows a **Lambda Architecture**, processing batch historical data for model training and real-time streaming data for inference.

### High-Level Data Flow





```text


+----------------+      +------------------+      +------------------+
|  DATA SOURCES  |      | INGESTION LAYER  |      |  LAKEHOUSE (S3)  |
+----------------+      +------------------+      +------------------+
|  Stock Market  |      |   Airflow DAGs   |      |  [Bronze] Raw    |
|   (VNStock)    +----->|     (Batch)      +----->|   JSON / HTML    |
|                |      |                  |      |        |         |
+----------------+      +------------------+      +--------+---------+
| Financial News |      | Redpanda / Kafka |      |  [Silver] Delta  |
|    (CafeF)     +----->|     (Stream)     +----->|   Clean Parquet  |
|                |      |                  |      |        |         |
+----------------+      +------------------+      +--------+---------+
                                                           |
                                                           v
+----------------+      +------------------+      +------------------+
|   PRESENTATION |      |   INTELLIGENCE   |      | WAREHOUSE (Gold) |
+----------------+      +------------------+      +------------------+
|    Streamlit   |      |   LLM Agent      |      |     Postgres     |
|   Dashboard    |<-----+    (Llama 3)     |<-----+    (dbt Marts)   |
|                |      |                  |      |                  |
+----------------+      +------------------+      +------------------+
|    FastAPI     |      |   XGBoost Model  |      |   Feature Store  |
|    Gateway     |<-----+      (ML)        |<-----+      (Feast)     |
+----------------+      +------------------+      +------------------+




================================================================================
                    OMNIFIN SYSTEM ARCHITECTURE V1.0
================================================================================

    [ 1. EXTERNAL ]             [ 2. INGESTION ]            [ 3. STORAGE ]
   +---------------+           +---------------+           +---------------+
   |   VNStock     | --------> |   Redpanda    | --------> |     MinIO     |
   | (Quant Data)  |           |    (Kafka)    |           |  (Raw Bucket) |
   +---------------+           +---------------+           +-------+-------+
                                                                   |
   +---------------+           +---------------+                   v
   |    CafeF      | --------> |    Airflow    |           +---------------+
   |  (Qual Data)  |           |   Scraper     | --------> | Apache Spark  |
   +---------------+           +---------------+           | (Processing)  |
                                                           +-------+-------+
                                                                   |
            +------------------------------------------------------+
            |
            v                                      v
   +----------------+                      +----------------+
   |   PostgreSQL   |                      |    Qdrant      |
   |   (Gold DB)    |                      |  (Vector DB)   |
   +--------+-------+                      +-------+--------+
            |                                      |
            v                                      v
   +----------------+                      +----------------+
   |     Feast      |                      |   RAG Context  |
   | (Feature Store)|                      |   Retrieval    |
   +--------+-------+                      +-------+--------+
            |                                      |
            |              [ 4. AI CORE ]          |
            +-------------------+------------------+
                                |
                                v
                       +----------------+
                       |  Llama 3 Agent |
                       | (Reasoning Eng)|
                       +--------+-------+
                                |
                                v
                       +----------------+
                       |    FastAPI     |
                       |   (Endpoint)   |
                       +----------------+
```

### 📂 Repository Structure
```text

OmniFin/
├── infrastructure/        # Terraform & Docker Compose
├── ingestion/             # Scrapers (CafeF) & Producers (Redpanda)
├── lakehouse/             # Spark Jobs & Delta Lake logic
├── warehouse/             # dbt project (SQL models)
├── feature_store/         # Feast definitions (feature_views.py)
├── mlops/                 # Training scripts, MLflow tracking, Evidently
├── agent/                 # RAG logic, Ollama integration, Qdrant
├── api/                   # FastAPI gateway
└── monitoring/            # Grafana dashboards & Prometheus
```

### 🚀 How to Run Locally
### 📝 License
Distributed under the MIT License. See LICENSE for more information.

