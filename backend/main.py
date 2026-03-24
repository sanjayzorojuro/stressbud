from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.services.gemini_service import get_chat_response, get_sos_chat_response, reset_syllabus_session
from pydantic import BaseModel
from typing import Literal

app = FastAPI(title="StressBud API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    mode: Literal["home", "sos", "syllabus"] = "home"

# Routes all chat — home, sos, and syllabus — by mode field
@app.post("/api/chat")
async def chat(request: ChatRequest):
    response = get_chat_response(request.message, mode=request.mode)
    return {"reply": response}

# Kept for backward compatibility
@app.post("/api/sos-chat")
async def sos_chat(request: ChatRequest):
    response = get_sos_chat_response(request.message)
    return {"reply": response}

# ── NEW: Syllabus dedicated endpoint ──
# Explicitly routes to syllabus mode — fully solves math, code, academic questions
@app.post("/api/syllabus-chat")
async def syllabus_chat(request: ChatRequest):
    response = get_chat_response(request.message, mode="syllabus")
    return {"reply": response}

# ── NEW: Syllabus session reset ──
# Called by frontend every time student enters Syllabus mode — clears chat history
@app.post("/api/syllabus-reset")
async def syllabus_reset():
    reset_syllabus_session()
    return {"status": "reset"}