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

```text

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
