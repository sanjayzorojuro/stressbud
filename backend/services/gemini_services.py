import google.generativeai as genai
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dotenv import load_dotenv
load_dotenv()
from models.chat_model import StressCategory, Message
from utils.prompts import SOS_PROMPT, PRESSURE_PROMPT, SYLLABUS_PROMPT, GENERAL_PROMPT
from typing import List

def get_system_prompt(category: StressCategory) -> str:
    prompts = {
        StressCategory.SOS: SOS_PROMPT,
        StressCategory.PRESSURE: PRESSURE_PROMPT,
        StressCategory.SYLLABUS: SYLLABUS_PROMPT,
        StressCategory.GENERAL: GENERAL_PROMPT,
    }
    return prompts.get(category, GENERAL_PROMPT)


def build_gemini_history(history: List[Message]) -> List[dict]:
    """Convert our message history to Gemini format."""
    gemini_history = []
    for msg in history:
        role = "user" if msg.role == "user" else "model"
        gemini_history.append({
            "role": role,
            "parts": [{"text": msg.content}]
        })
    return gemini_history


async def get_gemini_response(
    message: str,
    category: StressCategory,
    history: List[Message]
) -> str:
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return fallback_response(category)

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=get_system_prompt(category)
        )

        gemini_history = build_gemini_history(history)
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(message)
        return response.text

    except Exception as e:
        print(f"Gemini error: {e}")
        return fallback_response(category)


def fallback_response(category: StressCategory) -> str:
    """Fallback responses when API is unavailable."""
    fallbacks = {
        StressCategory.SOS: (
            "Hey, I hear you and I'm really glad you reached out. "
            "Whatever you're feeling right now is valid. "
            "Please take a slow breath with me — in for 4 counts, hold for 4, out for 4. "
            "You're not alone. 💙\n\n"
            "**Please reach out:** iCall: 9152987821 | Vandrevala: 1860-2662-345"
        ),
        StressCategory.PRESSURE: (
            "The pressure you're feeling is real and it makes complete sense. "
            "You don't have to be perfect — you just have to keep going. "
            "One small step at a time. What's ONE thing you can do right now to feel a tiny bit better?"
        ),
        StressCategory.SYLLABUS: (
            "Okay, let's breathe and make a plan! 📚 "
            "Start with the highest-weightage topic you feel most comfortable with. "
            "Set a 25-minute timer, close everything else, and just go. "
            "You'll be surprised how much you can cover. You've got this!"
        ),
        StressCategory.GENERAL: (
            "Hey, I'm StressBud and I'm here for you! 🌱 "
            "Exam season is tough, but you're tougher. "
            "Tell me what's going on — studies, pressure, or just feeling off?"
        ),
    }
    return fallbacks.get(category, fallbacks[StressCategory.GENERAL])