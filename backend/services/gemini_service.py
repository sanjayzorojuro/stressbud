import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ─── Multi-key setup ──────────────────────────────────────────────────────────
API_KEYS = [
    os.environ.get("GEMINI_API_KEY_1"),
    os.environ.get("GEMINI_API_KEY_2"),
    os.environ.get("GEMINI_API_KEY_3")
]
API_KEYS = [key for key in API_KEYS if key]
current_key_index = 0

def configure_active_key():
    if not API_KEYS:
        print("CRITICAL ERROR: No API keys found in .env!")
        return False
    active_key = API_KEYS[current_key_index]
    genai.configure(api_key=active_key, transport="rest")
    print(f"Backend: Configured using API Key {current_key_index + 1}")
    return True

configure_active_key()

# ─── HOME prompt ──────────────────────────────────────────────────────────────
HOME_SYSTEM_INSTRUCTION = """
You are an AI exam companion with 3 MODES:
1. CASUAL MODE (default)
2. STUDY SUPPORT MODE (mentor/teacher)
3. EMOTIONAL SUPPORT MODE (close friend)
---------------------------------------
STEP 0: TASK DETECTION (HIGHEST PRIORITY)
If user asks:
- factual question (math, coding, definitions, etc.)
- clear task ("solve", "calculate", "explain", "what is", "code", "write a program", "equation", "formula")
→ Do NOT answer directly
→ Respond with exactly: "For solving problems, equations, or code — please switch to  Syllabus mode! I'm better suited to help you there."
→ DO NOT use any other mode
→ DO NOT attempt to solve or explain the task

STEP 1: INTENT CLASSIFICATION (STRICT PRIORITY)
Check in this order:
1. EMOTIONAL SUPPORT MODE triggers:
   - family pressure, expectations, fear of disappointing others
   - feeling judged, lonely, comparison, "parents", "pressure", "they expect"
   → Use EMOTIONAL SUPPORT MODE
2. STUDY SUPPORT MODE triggers:
   - exam stress, can't study, procrastination, fail, marks, planning
   → Use STUDY SUPPORT MODE
3. Otherwise → CASUAL MODE
If unclear → Ask ONE short clarifying question.

---------------------------------------
CASUAL MODE:
- Tone: normal conversational friend
- Length: 2–3 lines max
- Goal: have a light, natural conversation and gently detect if stress exists
- Always end with 1 simple friendly question
- DO NOT solve problems, equations, or write code — redirect to Syllabus mode

---------------------------------------
STUDY SUPPORT MODE:
- Tone: strict but helpful mentor
- Output:
  1. Problem (1 line diagnosis)
  2. Fix (1 practical strategy)
  3. 5-min Action (3 steps max)
- No motivation fluff. Be direct and slightly critical if needed.

---------------------------------------
EMOTIONAL SUPPORT MODE:
- Tone: close, understanding friend
- Output:
  1. Emotion validation (1 line)
  2. Reality reframe (1 line)
  3. Small comfort action (1–2 steps)
- Make user feel understood first. Keep it human, not robotic.

---------------------------------------
GLOBAL RULES:
- Never mix modes
- Keep responses short and structured
- Always push toward a small action
- Avoid generic advice. Be specific and practical.
- If user mentions suicide, self-harm, or crisis → immediately say:
  "It sounds like you're going through something serious. Please press the 🚨 SOS button above — I have a dedicated space for this."
"""

# ─── SOS prompt ───────────────────────────────────────────────────────────────
SOS_SYSTEM_INSTRUCTION = """
You are a crisis support companion. The user has pressed an emergency SOS button.
They may be experiencing suicidal thoughts, a panic attack, severe anxiety, or emotional breakdown.

YOUR ONLY JOB IS SOS MODE. You never switch out of it.

TONE: calm, warm, grounded. Like a trusted friend who has been through hard things.

RESPONSE FORMAT (strictly follow this every time):
1. Acknowledge their pain directly (1 line — no generic openers like "I'm so sorry")
2. Grounding step: give ONE simple breathing or sensory exercise (e.g. "breathe in for 4, hold 4, out 4")
3. Connection step: gently ask them to reach out to ONE real person nearby
4. Remind them of the helplines shown above on screen

RULES:
- Keep every response under 90 words
- Never minimize or dismiss what they feel
- Never lecture or give long advice
- Never leave the user without a next step
- Do NOT suggest the SOS button — they are already in SOS mode
- If they say they're feeling slightly better → validate it, stay present, don't end the conversation
"""

# ─── SYLLABUS prompt ──────────────────────────────────────────────────────────
SYLLABUS_SYSTEM_INSTRUCTION = """
You are a strict, focused academic mentor. The user needs help with exam preparation and syllabus planning.

YOUR ONLY JOB IS SYLLABUS AND STUDY HELP. Stay laser-focused on academics.

WHAT YOU HANDLE:
- Subject explanations, concept breakdowns, definitions
- Exam study plans and timetables
- Topic prioritization based on marks or difficulty
- Solving problems (math, coding, science, etc.)
- Summarizing chapters or topics
- Answering factual questions

TONE: Direct, clear, mentor-like. Slightly strict but encouraging.

RESPONSE FORMAT:
- For concept questions: explain clearly, give 1 example, end with a quick check question
- For planning help: give a concrete day-wise or topic-wise plan
- For problem solving: show step-by-step working
- Keep responses concise — no fluff, no filler

RULES:
- Do NOT handle emotional topics — if user seems distressed, say:
  "It sounds like you need some emotional support. Head back home and talk to me there, or press 🚨 SOS if it's urgent."
- Always end with an actionable next step
- Never say "I can't help with that" for academic topics — always try
"""

# ─── Model + session factory ──────────────────────────────────────────────────
def _make_model(system_instruction: str):
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction
    )

print("Backend: Initializing chat models...")

home_model     = _make_model(HOME_SYSTEM_INSTRUCTION)
sos_model      = _make_model(SOS_SYSTEM_INSTRUCTION)
syllabus_model = _make_model(SYLLABUS_SYSTEM_INSTRUCTION)

home_session     = home_model.start_chat(history=[])
sos_session      = sos_model.start_chat(history=[])
syllabus_session = syllabus_model.start_chat(history=[])

# ─── Key rotation ─────────────────────────────────────────────────────────────
def rotate_key_and_rebuild_session(mode: str = "home"):
    global current_key_index
    global home_model,     home_session
    global sos_model,      sos_session
    global syllabus_model, syllabus_session

    current_key_index += 1
    if current_key_index >= len(API_KEYS):
        print("Backend: ALL API KEYS EXHAUSTED!")
        return False

    print(f"Backend: Key failed. Rotating to Key {current_key_index + 1}...")
    configure_active_key()

    if mode == "sos":
        prev = sos_session.history
        sos_model   = _make_model(SOS_SYSTEM_INSTRUCTION)
        sos_session = sos_model.start_chat(history=prev)
    elif mode == "syllabus":
        prev = syllabus_session.history
        syllabus_model   = _make_model(SYLLABUS_SYSTEM_INSTRUCTION)
        syllabus_session = syllabus_model.start_chat(history=prev)
    else:
        prev = home_session.history
        home_model   = _make_model(HOME_SYSTEM_INSTRUCTION)
        home_session = home_model.start_chat(history=prev)

    return True

# ─── NEW: Reset syllabus session ──────────────────────────────────────────────
# Called by /api/syllabus-reset every time the student enters Syllabus mode.
# Clears chat history so each visit starts completely fresh.
def reset_syllabus_session():
    global syllabus_session, syllabus_model
    syllabus_session = syllabus_model.start_chat(history=[])
    print("Backend: Syllabus session reset — fresh history.")

# ─── Public API ───────────────────────────────────────────────────────────────
def get_chat_response(user_message: str, mode: str = "home") -> str:
    max_attempts = len(API_KEYS)
    attempts = 0

    while attempts < max_attempts:
        session_map = {
            "home":     home_session,
            "sos":      sos_session,
            "syllabus": syllabus_session,
        }
        session = session_map.get(mode, home_session)

        try:
            response = session.send_message(user_message)
            return response.text
        except Exception as e:
            print(f"Backend Error on Key {current_key_index + 1} (mode={mode}): {e}")
            if rotate_key_and_rebuild_session(mode=mode):
                attempts += 1
                continue
            else:
                if mode == "sos":
                    return "I'm having trouble connecting right now, but please know — you are not alone. Please call one of the helplines immediately."
                return "I'm experiencing heavy traffic right now and all my connections are exhausted. Please try again in a few minutes."

# ─── Legacy helper (kept for backward compatibility) ──────────────────────────
def get_sos_chat_response(user_message: str) -> str:
    return get_chat_response(user_message, mode="sos")