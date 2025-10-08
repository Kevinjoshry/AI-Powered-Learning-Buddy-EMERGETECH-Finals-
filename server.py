# server.py
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()

API_KEY = "AIzaSyA4skjWkL4Snn-_tWFYLoRIy2XHnC_rAoo"
client = genai.Client(api_key=API_KEY)

class ChatRequest(BaseModel):
    message: str
    history: list

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        # Build prompt from chat history
        history_text = "\n".join([f"{h['role']}: {h['content']}" for h in req.history])
        full_prompt = f"{history_text}\nuser: {req.message}"

        # ✅ Use correct model name for the new SDK
        response = client.models.generate_content(
            model="models/gemini-1.5-flash-latest",
            contents=full_prompt
        )

        reply = response.text
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"⚠️ Error: {e}"}
