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
    
    try:
        # Tenta usar diretamente o gemini-2.5-flash
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"Responda como um assistente de TI profissional e direto: {req.message}"
        response = model.generate_content(prompt)
        
        if response and response.text:
            return {"response": response.text}
            
    except Exception as e:
        return {"response": f"Erro na Google API: {str(e)}"}
        
    return {"response": "Não foi possível gerar resposta."}
