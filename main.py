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

@app.post("/chat")
def chat(req: MessageRequest):
    if not GEMINI_API_KEY:
        return {"response": "Erro: GEMINI_API_KEY não configurada no Render."}
    
    genai.configure(api_key=GEMINI_API_KEY.strip())
    
    # Lista de modelos para tentar caso um atinja o limite de requisições (Quota 429)
    models_fallback = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    
    for model_name in models_fallback:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(req.message)
            if response and response.text:
                return {"response": response.text}
        except Exception as e:
            continue
            
    return {"response": "Limite de requisições atingido. Aguarde alguns segundos e tente novamente."}
