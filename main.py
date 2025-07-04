from fastapi import FastAPI, Request
import requests
from fastapi.responses import JSONResponse
import os

app = FastAPI()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/")
def root():
    return {"message": "Alive ✅"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4",  # You can change to 'mistral/mistral-7b-instruct' etc.
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        reply = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Error: {str(e)}"

    return JSONResponse(content={"reply": reply})
