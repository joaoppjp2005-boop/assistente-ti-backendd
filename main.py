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
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não configurada no Render.")
    
    clean_key = GEMINI_API_KEY.strip()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={clean_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Responda como um assistente de TI: {req.message}"
            }]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        data = response.json()
        
        # Corrigido o operador para !=
        if response.status_code != 200:
            print("ERRO DETALHADO DA GOOGLE:", data)
            error_msg = data.get("error", {}).get("message", "Erro na API do Gemini")
            raise HTTPException(status_code=500, detail=f"Erro da API Google: {error_msg}")
            
        ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"response": ai_response}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print("EXCECAO NO SERVIDOR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
