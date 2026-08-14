# Zepto Capstone-Data, Analytics & GenAI Pipeline
Zepto Capstone Project

An end-to-end data engineering, analytics, machine learning, and GenAI project built around a Zepto-style product and support workflow.

**Project Overview**

This capstone project is organized into three independent but related modules:

1. Data Pipeline — scrape, clean, transform, store, and validate catalog data.
2. Analytics & Machine Learning — perform exploratory analysis and build predictive models using the Titanic dataset.
3. Support Assistant — build an offline RAG-based Zepto policy assistant using local embeddings, ChromaDB, LangGraph, Pydantic, and FastAPI.

Repository Structure

**Module 1** — Data Pipeline

The data pipeline demonstrates a complete raw-to-relational workflow:

Scrape → Clean → Convert → Store → Query → Validate

Data is collected programmatically from Books to Scrape using "requests" and "BeautifulSoup".

The cleaned catalog is stored in a normalized SQLite database with separate category and book tables. SQL queries are executed against the database and their results are validated independently using pandas.

The required fixed currency conversion is:

1 GBP = 105.50 INR

See ""data_pipeline/README.md"" (data_pipeline/README.md) for implementation details and run instructions.

**Module 2** — Analytics & Machine Learning

The analytics module follows an analyst-to-data-scientist workflow:

Load → Profile → Clean → Explore → Model → Evaluate → Tune → Persist

The Titanic dataset is analyzed through EDA, missing-value handling, outlier analysis, correlation analysis, visualization, classification, class-imbalance comparison, hyperparameter tuning, and regression.

Three classification models are evaluated:

- Logistic Regression
- Decision Tree
- Random Forest

The final fitted preprocessing-and-model pipeline is persisted using "joblib".

See ""analytics/README.md"" (analytics/README.md) for detailed results and conclusions.

**Module 3** - Zepto Support Assistant

The support assistant implements an offline Retrieval-Augmented Generation pipeline:

Documents → Chunking → Local Embeddings → ChromaDB → LangGraph Routing → Retrieval → Structured Response → FastAPI

Eight Zepto policy documents are embedded locally using "all-MiniLM-L6-v2" and stored in ChromaDB.

The application uses deterministic "MOCK_LLM=1" mode as the required offline baseline, so no external LLM API key is required.

The service exposes a FastAPI "POST /ask" endpoint and includes a Dockerfile for local container execution.

See ""support_assistant/README.md"" (support_assistant/README.md) for architecture, examples, and run instructions.

**Key Technologies**

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite
- SQL
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Imbalanced-learn
- Joblib
- Sentence Transformers
- ChromaDB
- LangGraph
- Pydantic
- FastAPI
- Docker
- Jupyter / Google Colab

**Reproducibility**

Each module contains its own README with installation and execution instructions.

The project is designed so that:

- The data pipeline can recreate its SQLite database from the source data.
- The analytics module includes "titanic.csv" as an offline fallback dataset.
- The support assistant uses local embeddings and deterministic mock logic for its required baseline.
- No external LLM API is required for the graded support-assistant path.

**Summary**

This project demonstrates an end-to-end workflow spanning:

Data Engineering → Data Analytics → Machine Learning → Generative AI / RAG → API Deployment

Each module is independently organized while remaining part of the same capstone repository.
