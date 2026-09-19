import os
from fastapi import FastAPI, HTTPException
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
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Backend online!"}

@app.post("/chat")
def chat(req: MessageRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY não configurada no Render.")
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            "Tu és um Assistente Virtual especializado em Suporte de TI e computadores. "
            "Responde de forma clara e objetiva à seguinte dúvida do utilizador: "
            f"{req.message}"
        )
        
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
