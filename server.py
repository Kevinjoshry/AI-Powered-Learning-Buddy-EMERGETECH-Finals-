# server.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

# Initialize FastAPI
app = FastAPI()

# ✅ Allow Streamlit frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8501"] if you want to be strict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load Gemini API key correctly
API_KEY = os.getenv("GEMINI_API_KEY")  # safer way to load key from environment variable
client = genai.Client(api_key=API_KEY)

# Define request format
class ChatRequest(BaseModel):
    message: str
    history: list  # list of {"role": "user"|"assistant", "content": "..."}

@app.post("/chat")
async def chat(req: ChatRequest):
    messages = [
        {"role": "system", "content": "You are a helpful AI learning assistant that explains quiz concepts clearly."}
    ] + req.history + [{"role": "user", "content": req.message}]

    try:
        response = client.chat.completions.create(
            model="gemini-1.5-flash",  # you can also use gemini-1.5-pro for higher quality
            messages=messages
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"Sorry, I encountered an error: {e}"

    return {"reply": reply}
