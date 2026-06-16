import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Force gRPC to use native IPv4 resolver to prevent network timeouts
os.environ["GRPC_DNS_RESOLVER"] = "native"

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY is missing from your .env file!")

genai.configure(api_key=GEMINI_API_KEY)