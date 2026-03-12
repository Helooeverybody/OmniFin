# 🏦 OmniFin: Autonomous Financial Intelligence Platform


![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Spark](https://img.shields.io/badge/Apache_Spark-Streaming-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)


> **A Unified Data Lakehouse & MLOps Platform combining Quantitative Market Data with Qualitative News Sentiment to generate Explainable Investment Strategies.**

---

## 📖 Executive Summary

**OmniFin** is an enterprise-grade financial data platform designed to mimic the architecture of modern Fintech unicorns. It solves the challenge of **Multimodal Financial Analysis** by ingesting real-time stock ticks (Quantitative) and unstructured financial news (Qualitative) into a unified **Lakehouse**.

Unlike traditional black-box models, OmniFin utilizes an **Agentic RAG (Retrieval-Augmented Generation)** approach, where a Large Language Model (Llama 3) acts as a portfolio manager, synthesizing technical indicators from the Feature Store with news sentiment from the Vector Database to provide **explainable trading signals** compliant with financial auditing standards.

---

## 🏗️ System Architecture

The platform follows a **Lambda Architecture**, processing batch historical data for model training and real-time streaming data for inference.


<img width="2020" height="853" alt="pipeline" src="https://github.com/user-attachments/assets/22adab28-f94d-43d2-a49a-3f84b501906c" />



## 📂 Repository Structure
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

## 🚀 How to Run Locally
## 📝 License
Distributed under the MIT License. See LICENSE for more information.

