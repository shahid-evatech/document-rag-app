# Document Q&A Engine (RAG Prototype)

A lightweight, modular Retrieval-Augmented Generation (RAG) system built with **FastAPI** and **Google Gemini AI**. The application allows users to upload `.txt` or `.pdf` documents, chunks the content, processes semantic embeddings, and handles grounded Q&A through an interactive UI without hallucinating.

## 📦 Dependencies & Package Breakdown

The core engine relies on a lightweight, production-ready stack designed for fast math operations and asynchronous API routing:

* **`fastapi`**: A modern, fast (high-performance) web framework for building APIs with Python based on standard Python type hints. It orchestrates our `/upload` and `/ask` routes.
* **`uvicorn`**: An production-grade ASGI web server implementation for Python, used to serve and reload our FastAPI application instance.
* **`google-generativeai`**: The official Google GenAI Python SDK. It handles communication with the remote Gemini API endpoint to retrieve document embeddings (`models/gemini-embedding-001`) and generate grounded text generation responses (`models/gemini-2.5-flash`).
* **`python-multipart`**: Enables FastAPI to parse and process multi-part form data, allowing users to stream files via HTTP POST data inputs.
* **`numpy`**: A fundamental library for scientific computing in Python. It converts raw array lists into optimized memory structures to compute vector-based cosine similarity logic over high-dimensional spaces natively in C speed.
* **`pypdf`**: A pure-Python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files. In this app, it reads incoming binary files and extracts raw text data from PDF documents.
* **`python-dotenv`**: Reads key-value pairs from a local `.env` file and sets them as environment variables, securely decoupling production credentials from application code.

## 🏗️ Architecture Design

The application is structured following clean, modular engineering separation of concerns:
* `main.py`: The orchestration layer managing API endpoints (`/`, `/upload`, `/ask`) and in-memory state.
* `utils.py`: Core computational logic including overlapping text segmentation, embedding generation, and vector cosine similarity.
* `config.py`: Environment management and system network optimization overrides.
* `ui.py`: Isolated frontend user interface layer.

---

## 🛠️ Setup & Installation

### 1. Clone & Enter Project Directory
```bash
cd document-rag-app