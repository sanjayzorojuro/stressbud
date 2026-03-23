import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.chat_model import StressCategory

# Keywords for each stress category
SOS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm", "self-harm",
    "cut myself", "hurt myself", "don't want to live", "want to die",
    "no point living", "panic attack", "can't breathe", "anxiety attack",
    "breaking down", "can't take it", "losing my mind", "hopeless",
    "worthless", "nobody cares", "disappear", "not okay", "help me"
]

PRESSURE_KEYWORDS = [
    "parents", "family", "mom", "dad", "disappointed", "expectations",
    "peer pressure", "friends", "comparison", "topper", "rank",
    "teacher", "professor", "college", "school", "ashamed", "failure",
    "let down", "not enough", "embarrassed", "judged", "reputation"
]

SYLLABUS_KEYWORDS = [
    "syllabus", "chapters", "pending", "revision", "notes", "exam",
    "test", "haven't studied", "not prepared", "last minute", "cramming",
    "portions", "topics", "forgot", "blanked out", "time", "deadlines",
    "assignment", "project", "marks", "score", "pass", "fail", "study"
]


def detect_category(message: str) -> StressCategory:
    """Detect the stress category from the user message."""
    msg_lower = message.lower()

    # Check SOS first — highest priority
    sos_score = sum(1 for kw in SOS_KEYWORDS if kw in msg_lower)
    pressure_score = sum(1 for kw in PRESSURE_KEYWORDS if kw in msg_lower)
    syllabus_score = sum(1 for kw in SYLLABUS_KEYWORDS if kw in msg_lower)

    if sos_score > 0:
        return StressCategory.SOS
    elif pressure_score >= syllabus_score and pressure_score > 0:
        return StressCategory.PRESSURE
    elif syllabus_score > 0:
        return StressCategory.SYLLABUS
    else:
        return StressCategory.GENERAL


def is_crisis(message: str) -> bool:
    """Check if the message indicates a crisis situation."""
    CRISIS_KEYWORDS = [
        "suicide", "kill myself", "end my life", "self harm", "self-harm",
        "cut myself", "hurt myself", "don't want to live", "want to die",
        "no point living", "not worth living"
    ]
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in CRISIS_KEYWORDS)


def get_resources_for_category(category: StressCategory) -> list:
    """Return relevant resources based on the stress category."""
    resources = {
        StressCategory.SOS: [
            {"title": "iCall Helpline", "detail": "9152987821", "type": "helpline"},
            {"title": "Vandrevala Foundation", "detail": "1860-2662-345 (24/7)", "type": "helpline"},
            {"title": "Box Breathing Exercise", "detail": "Inhale 4s → Hold 4s → Exhale 4s → Hold 4s", "type": "technique"},
            {"title": "5-4-3-2-1 Grounding", "detail": "Name 5 things you see, 4 you hear, 3 you can touch, 2 you smell, 1 you taste", "type": "technique"},
        ],
        StressCategory.PRESSURE: [
            {"title": "Reframe Exercise", "detail": "Write down the pressure thought, then rewrite it kindly as if talking to a friend", "type": "technique"},
            {"title": "2-Minute Journal", "detail": "Write 3 things you're proud of today — no matter how small", "type": "technique"},
            {"title": "Talk to Someone", "detail": "A counselor, trusted friend, or iCall: 9152987821", "type": "helpline"},
        ],
        StressCategory.SYLLABUS: [
            {"title": "Pomodoro Technique", "detail": "25 min study → 5 min break. Repeat 4 times, then take a 20 min break", "type": "technique"},
            {"title": "Priority Matrix", "detail": "Sort topics: High marks + Easy = Do first. High marks + Hard = Do second", "type": "technique"},
            {"title": "The 1-Page Summary Method", "detail": "Summarize each chapter in 1 page — forces you to extract only what matters", "type": "technique"},
        ],
        StressCategory.GENERAL: [
            {"title": "StressBud Tip", "detail": "Take a 5-minute walk, drink water, and come back. You've got this.", "type": "tip"},
        ],
    }
    return resources.get(category, [])