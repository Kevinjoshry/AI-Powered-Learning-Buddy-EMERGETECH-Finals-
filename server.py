# server.py
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# Configure API key
API_KEY = "AIzaSyA4skjWkL4Snn-_tWFYLoRIy2XHnC_rAoo"
genai.configure(api_key=API_KEY)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: list

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        # Combine history and user message
        history_text = "\n".join([f"{h['role']}: {h['content']}" for h in req.history])
        full_prompt = f"{history_text}\nuser: {req.message}"

        # ✅ Use correct model initialization
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        # ✅ Generate AI response
        response = model.generate_content(full_prompt)

        # Extract text safely
        reply = response.text if hasattr(response, "text") else "⚠️ No text returned from model."

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"⚠️ Error: {e}"}
