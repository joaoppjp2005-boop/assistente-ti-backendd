import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

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
    genai.configure(api_key=clean_key)
    
    try:
        # Usa o gemini-1.5-flash que é ultra-rápido na geração de texto
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(req.message)
        
        if response and response.text:
            return {"response": response.text}
            
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "Quota exceeded" in error_str:
            return {"response": "Limite de requisições temporariamente atingido. Aguarde cerca de 1 minuto e tente novamente."}
        return {"response": f"Erro na Google API: {error_str}"}
        
    return {"response": "Não foi possível gerar resposta."}
