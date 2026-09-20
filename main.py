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
    
    # Lista de modelos alternativos para garantir resposta rápida
    models = ["gemini-1.5-flash", "gemini-1.5-pro"]
    
    for model_name in models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(req.message)
            if response and response.text:
                return {"response": response.text}
        except Exception as e:
            continue
            
    return {"response": "Não foi possível obter resposta no momento. Tente novamente em instantes."}
