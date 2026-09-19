import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Backend online!"}

@app.post("/chat")
def chat(req: MessageRequest):
    if not GEMINI_API_KEY:
        return {"response": "Erro: GEMINI_API_KEY não configurada no Render."}
    
    clean_key = GEMINI_API_KEY.strip()
    
    # Modelo oficial corrigido: gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={clean_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Responda como um assistente de TI de forma clara e objetiva: {req.message}"
            }]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        data = response.json()
        
        if response.status_code != 200:
            error_msg = data.get("error", {}).get("message", "Erro desconhecido na API do Gemini")
            return {"response": f"Erro da Google ({response.status_code}): {error_msg}"}
            
        ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"response": ai_response}
        
    except Exception as e:
        return {"response": f"Erro interno do servidor: {str(e)}"}
