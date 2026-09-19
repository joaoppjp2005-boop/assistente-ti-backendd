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
    
    # Lista de modelos para tentar (do mais recente para o mais genérico)
    models_to_try = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-pro",
        "models/gemini-1.5-flash"
    ]
    
    last_error = ""
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = f"Responda como um assistente de TI profissional e direto: {req.message}"
            response = model.generate_content(prompt)
            if response and response.text:
                return {"response": response.text}
        except Exception as e:
            last_error = str(e)
            continue
            
    return {"response": f"Erro na Google API ao chamar modelos: {last_error}"}
