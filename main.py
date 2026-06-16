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

app = FastAPI(title="Document RAG Application")

# Global In-Memory Vector Storage
VECTOR_DATABASE = []

class AskRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def frontend_ui():
    return get_frontend_html()

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
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
        return {"error": "File is empty or content unreadable."}
        
    # Process and build internal database
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        VECTOR_DATABASE.append({
            "id": i,
            "text": chunk.strip(),
            "embedding": get_embedding(chunk)
        })
        
    return {"message": f"Successfully loaded {len(chunks)} chunks!"}

@app.post("/ask")
def ask_question(request: AskRequest):
    global VECTOR_DATABASE
    if not VECTOR_DATABASE:
        return {"answer": "Upload a document first.", "sources": []}
        
    try:
        # Calculate semantic matching scores
        q_embedding = get_embedding(request.question)
        scored = []
        for chunk in VECTOR_DATABASE:
            score = cosine_similarity(q_embedding, chunk["embedding"])
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
        
        return {
            "answer": response.text.strip(),
            "sources": [c[1] for c in top_chunks]
        }
    except RuntimeError as custom_err:
        return {"answer": f"Error: {custom_err}", "sources": []}
    except Exception:
        return {"answer": "A network timeout occurred. Please try your question again.", "sources": []}