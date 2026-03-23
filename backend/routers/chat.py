from fastapi import APIRouter
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.chat_model import ChatRequest, ChatResponse, StressCategory
from services.sentiment_service import detect_category, is_crisis, get_resources_for_category
from services.gemini_services import get_gemini_response
import uuid

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())

    # Detect stress category
    category = detect_category(request.message)

    # Check for crisis
    crisis = is_crisis(request.message)

    # Get AI response
    reply = await get_gemini_response(
        message=request.message,
        category=category,
        history=request.history or []
    )

    # Get relevant resources
    resources = get_resources_for_category(category)

    return ChatResponse(
        reply=reply,
        category=category,
        session_id=session_id,
        resources=resources,
        is_crisis=crisis
    )


@router.get("/categories")
def get_categories():
    return {
        "categories": [
            {"id": "sos", "label": "SOS / Mental Health", "emoji": "🆘"},
            {"id": "pressure", "label": "Pressure & Expectations", "emoji": "😤"},
            {"id": "syllabus", "label": "Syllabus & Studies", "emoji": "📚"},
            {"id": "general", "label": "General Stress", "emoji": "💬"},
        ]
    }