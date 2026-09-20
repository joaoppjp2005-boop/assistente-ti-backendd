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
        return {"response": "Erro: GEMINI_API_KEY não foi configurada nas variáveis do Render."}
    
    try:
        clean_key = GEMINI_API_KEY.strip()
        genai.configure(api_key=clean_key)
        
        # Tenta modelos compatíveis em ordem
        models_to_try = ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-pro"]
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(req.message)
                if response and response.text:
                    return {"response": response.text}
            except Exception:
                continue
                
        return {"response": "Não foi possível gerar uma resposta com os modelos disponíveis."}
            
    except Exception as e:
        return {"response": f"Erro na API do Gemini: {str(e)}"}
