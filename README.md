# Document Q&A Engine (RAG Prototype)

A lightweight Retrieval-Augmented Generation (RAG) application built with **FastAPI** and **Google Gemini AI**. The application enables users to upload `.txt` and `.pdf` documents, generates semantic embeddings for the document content, and answers questions using information retrieved from the uploaded document.

The project is designed to demonstrate the core RAG workflow, including document ingestion, text chunking, embedding generation, vector similarity search, and grounded response generation.

---

## 📦 Dependencies

| Package                 | Purpose                                                                  |
| ----------------------- | ------------------------------------------------------------------------ |
| **FastAPI**             | Builds the REST API and handles application routing.                     |
| **Uvicorn**             | ASGI server used to run the FastAPI application.                         |
| **google-generativeai** | Google Gemini SDK used for generating embeddings and grounded responses. |
| **python-multipart**    | Enables file uploads through FastAPI.                                    |
| **NumPy**               | Performs vector operations and cosine similarity calculations.           |
| **PyPDF**               | Extracts text from uploaded PDF documents.                               |
| **python-dotenv**       | Loads environment variables from a local `.env` file.                    |

---

## 🏗️ Project Structure

```
.
├── main.py        # FastAPI application and API endpoints
├── utils.py       # Chunking, embeddings, and similarity search
├── config.py      # Environment configuration
├── ui.py          # Frontend UI
├── .env           # Environment variables (not committed)
└── README.md
```

### File Responsibilities

* **main.py** – Defines the application, API routes, and request handling.
* **utils.py** – Contains the document processing pipeline, embedding generation, and vector similarity logic.
* **config.py** – Loads configuration values and environment variables.
* **ui.py** – Implements the user interface.

---

## 🚀 Features

* Upload `.txt` and `.pdf` documents
* Automatic document text extraction
* Text chunking for efficient retrieval
* Semantic embeddings using Google Gemini
* Cosine similarity search
* Grounded question answering using retrieved document context
* Simple FastAPI-based web interface

---

## 🛠️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shahid-evatech/document-rag-app.git
cd document-rag-app
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment


```bash
source venv/bin/activate
```
### 4. Install Dependencies

```bash
pip install fastapi uvicorn google-generativeai python-multipart numpy pypdf python-dotenv
```

### 5. Configure Environment Variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 6. Run the Application

```bash
uvicorn main:app --reload
```

The application will start at:

```
http://127.0.0.1:8000
```

---

## 🔄 Application Workflow

1. Upload a `.txt` or `.pdf` document.
2. Extract text from the uploaded file.
3. Split the document into overlapping chunks.
4. Generate embeddings for each chunk using Gemini.
5. Store embeddings in memory.
6. Convert the user's question into an embedding.
7. Retrieve the most relevant document chunks using cosine similarity.
8. Generate a grounded answer using the retrieved context.

---


