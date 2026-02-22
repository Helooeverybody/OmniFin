# 🏦 OmniFin: Autonomous Financial Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
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

```mermaid
graph TD
    %% Nodes
    subgraph Sources ["📡 Data Sources"]
        News[CafeF / Google News]
        Stocks[VNStock / Yahoo]
    end

    subgraph Ingestion ["Hz Ingestion Layer"]
        Airflow[Apache Airflow<br/>(Batch Scheduling)]
        Redpanda[Redpanda / Kafka<br/>(Real-Time Stream)]
    end

    subgraph Lakehouse ["💾 Data Lakehouse (MinIO)"]
        Bronze[(Bronze Layer<br/>Raw JSON)]
        Silver[(Silver Layer<br/>Delta Lake)]
        Gold[(Gold Layer<br/>Postgres/dbt Marts)]
    end

    subgraph Intelligence ["🧠 AI & MLOps Cortex"]
        Feast[Feast Feature Store]
        XGB[XGBoost Model]
        VectorDB[(Qdrant Vector DB)]
        LLM[Llama 3 Agent]
    end

    %% Connections
    News --> Airflow & Redpanda
    Stocks --> Redpanda
    
    Airflow --> Bronze
    Redpanda --> Bronze
    
    Bronze -->|Spark| Silver
    Silver -->|dbt| Gold
    
    Gold --> Feast
    News -->|Embedding| VectorDB
    
    Feast --> XGB
    XGB -->|Prediction| LLM
    VectorDB -->|Context| LLM
