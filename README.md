# OmniFin


graph TD
    %% Define Styles
    classDef source fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef ingest fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef storage fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef ml fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef serve fill:#ffebee,stroke:#c62828,stroke-width:2px;

    %% Nodes
    subgraph Sources ["📡 Data Sources"]
        News[CafeF / Google News]:::source
        Stocks[VNStock / Yahoo]:::source
    end

    subgraph Ingestion ["Hz Ingestion Layer"]
        Airflow[Apache Airflow<br/>(Batch Scheduling)]:::ingest
        Redpanda[Redpanda / Kafka<br/>(Real-Time Stream)]:::ingest
    end

    subgraph Lakehouse ["💾 Data Lakehouse (MinIO)"]
        Bronze[(Bronze Layer<br/>Raw JSON)]:::storage
        Silver[(Silver Layer<br/>Delta Lake/Parquet)]:::storage
        Gold[(Gold Layer<br/>Postgres/dbt Marts)]:::storage
        VectorDB[(Qdrant<br/>Vector Embeddings)]:::storage
    end

    subgraph Intelligence ["🧠 AI & MLOps Cortex"]
        Feast[Feast Feature Store]:::ml
        XGB[XGBoost Model<br/>(Price Prediction)]:::ml
        LLM[Llama 3 Agent<br/>(Reasoning Engine)]:::ml
    end

    subgraph UserInterface ["🖥️ Presentation"]
        API[FastAPI Gateway]:::serve
        UI[Streamlit Dashboard]:::serve
    end

    %% Connections
    News --> Airflow
    Stocks --> Redpanda
    
    Airflow -->|Daily Batch| Bronze
    Redpanda -->|Stream| Bronze
    
    Bronze -->|Spark Job| Silver
    Silver -->|dbt Transformation| Gold
    
    Gold --> Feast
    News -->|Embedding| VectorDB
    
    Feast --> XGB
    XGB -->|Prediction| LLM
    VectorDB -->|Context Retrieval| LLM
    
    LLM --> API
    API --> UI
