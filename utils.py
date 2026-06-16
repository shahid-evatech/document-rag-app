import numpy as np
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError, RetryError

def chunk_text(text: str, chunk_size: int = 600, chunk_overlap: int = 100) -> list[str]:
    """Splits a string into overlapping manageable text chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def get_embedding(text: str) -> list[float]:
    """Generates vector embeddings using Gemini's stable embedding model."""
    try:
        result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except (RetryError, GoogleAPICallError) as net_err:
        print(f"⚠️ Network error generating embedding: {net_err}")
        raise RuntimeError("The AI embedding service is temporarily unreachable. Please try again.")

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Computes semantic similarity between two vectors."""
    arr1 = np.array(v1)
    arr2 = np.array(v2)
    return float(np.dot(arr1, arr2) / (np.linalg.norm(arr1) * np.linalg.norm(arr2)))