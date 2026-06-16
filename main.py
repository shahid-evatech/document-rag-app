import io
import config  # Triggers network configuration and Gemini initialization
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pypdf import PdfReader
import google.generativeai as genai

# Import modular helper elements
from ui import get_frontend_html
from utils import chunk_text, get_embedding, cosine_similarity
from schemas import UploadSuccessResponse, QueryAnswerResponse

app = FastAPI(
    title="Document Q&A RAG Engine",
    description="A lightweight, modular Retrieval-Augmented Generation prototype utilizing Gemini AI.",
    version="1.0.0"
)
# Global In-Memory Vector Storage
VECTOR_DATABASE = []

class AskRequest(BaseModel):
    question: str

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import io
from pypdf import PdfReader
import google.generativeai as genai

# Import your custom modules and decoupled schemas
from utils import chunk_text, get_embedding, cosine_similarity
from schemas import UploadSuccessResponse, QueryAnswerResponse, AskRequest

app = FastAPI(
    title="Document Q&A RAG Engine",
    description="A lightweight, modular Retrieval-Augmented Generation prototype utilizing Gemini AI.",
    version="1.0.0"
)

VECTOR_DATABASE = []

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def frontend_ui():
    # Calling your frontend layout function from ui.py
    from ui import get_frontend_html
    return get_frontend_html()


@app.post(
    "/upload", 
    response_model=UploadSuccessResponse,  # <-- Toggles clean Swagger schema definitions
    tags=["Document Management"],
    summary="Upload and index source documents"
)
async def upload_document(file: UploadFile = File(...)):
    """
    Ingests, segments, and vector-indexes a target document.
    
    - Accepts **.txt** or **.pdf** source files.
    - Employs a sliding-window text chunker locally.
    - Generates vector matrices using Gemini's specific **retrieval_document** task type.
    - Securely caches numerical vectors in-memory for instant asymmetric retrieval.
    """
    global VECTOR_DATABASE
    VECTOR_DATABASE.clear()
    
    contents = await file.read()
    text = ""
    
    # Text Extraction
    if file.filename.endswith(".pdf"):
        pdf_stream = io.BytesIO(contents)
        reader = PdfReader(pdf_stream)
        for page in reader.pages:
            t = page.extract_text()
            if t: 
                text += t + "\n"
    else:
        text = contents.decode("utf-8", errors="ignore")
        
    if not text.strip():
        raise HTTPException(status_code=400, detail="File is empty or content unreadable.")
        
    # Process and build internal database
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        VECTOR_DATABASE.append({
            "id": i,
            "text": chunk.strip(),
            "embedding": get_embedding(chunk, task_type="retrieval_document")
        })
        
    # Matches the return structure contract defined in your UploadSuccessResponse schema
    return {
        "status": "success",
        "message": f"Successfully loaded {len(chunks)} chunks!",
        "filename": file.filename
    }


@app.post(
    "/ask", 
    response_model=QueryAnswerResponse,  # <-- Toggles clean Swagger schema definitions
    tags=["Core RAG Engine"],
    summary="Query the document context pipeline"
)
def ask_question(request: AskRequest):
    """
    Processes a natural language prompt against the stored document vector matrix.
    
    - Converts input string into an embedding utilizing Gemini's specific **retrieval_query** task type.
    - Computes custom vector **Cosine Similarity** math across the high-dimensional cache space.
    - Enforces rigid prompt guardrails to fully suppress LLM hallucinations.
    - Returns a verifiable answer paired directly alongside the exact matching **source citation**.
    """
    global VECTOR_DATABASE
    if not VECTOR_DATABASE:
        return {
            "query": request.question,
            "answer": "Upload a document first.", 
            "source_chunk": ""
        }
        
    try:
        # Calculate semantic matching scores
        query_embedding = get_embedding(request.question, task_type="retrieval_query")

        scored = []
        for chunk in VECTOR_DATABASE:
            score = cosine_similarity(query_embedding, chunk["embedding"])
            scored.append((score, chunk["text"]))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        top_chunks = scored[:5]
        
        context_text = "\n\n".join([c[1] for c in top_chunks])
        
        # Grounding system parameters
        system_prompt = (
            "You are a strict assistant. Answer the question using ONLY the context provided below.\n"
            "If the context does not contain the answer, reply exactly with: 'I couldn't find that.'\n"
            f"Context:\n{context_text}"
        )
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(f"{system_prompt}\n\nQuestion: {request.question}")
        
        # Matches the return structure contract defined in your QueryAnswerResponse schema
        return {
            "query": request.question,
            "answer": response.text.strip(),
            "source_chunk": top_chunks[0][1] if top_chunks else ""  # Returns the best source chunk
        }
    except RuntimeError as custom_err:
        raise HTTPException(status_code=503, detail=f"Error: {custom_err}")
    except Exception:
        raise HTTPException(status_code=500, detail="A network timeout occurred. Please try your question again.")