import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Permite chamadas de qualquer origem (Vercel, local, etc.)
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
        return {"response": "Erro: GEMINI_API_KEY não foi configurada no Render."}
    
    try:
        clean_key = GEMINI_API_KEY.strip()
        genai.configure(api_key=clean_key)
        
        # Modelo mais rápido e moderno
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(req.message)
        
        if response and response.text:
            return {"response": response.text}
        else:
            return {"response": "Não foi possível obter resposta do Gemini."}
            
    except Exception as e:
        print("Erro interno:", str(e))
        return {"response": f"Erro na API do Gemini: {str(e)}"}
