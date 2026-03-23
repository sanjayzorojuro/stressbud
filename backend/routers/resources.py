from fastapi import APIRouter

router = APIRouter()

@router.get("/resources")
def get_all_resources():
    return {
        "helplines": [
            {"name": "iCall", "number": "9152987821", "hours": "Mon-Sat, 8am-10pm"},
            {"name": "Vandrevala Foundation", "number": "1860-2662-345", "hours": "24/7"},
            {"name": "NIMHANS", "number": "080-46110007", "hours": "24/7"},
            {"name": "Snehi", "number": "044-24640050", "hours": "24/7"},
        ],
        "techniques": [
            {
                "name": "Box Breathing",
                "steps": ["Inhale for 4 seconds", "Hold for 4 seconds", "Exhale for 4 seconds", "Hold for 4 seconds"],
                "duration": "2 minutes",
                "for": "anxiety, panic"
            },
            {
                "name": "5-4-3-2-1 Grounding",
                "steps": ["5 things you see", "4 things you hear", "3 things you can touch", "2 things you smell", "1 thing you taste"],
                "duration": "3 minutes",
                "for": "panic attacks, overwhelm"
            },
            {
                "name": "Pomodoro Technique",
                "steps": ["Study for 25 minutes", "Take a 5-minute break", "Repeat 4 times", "Take a 20-minute break"],
                "duration": "Flexible",
                "for": "syllabus stress, procrastination"
            },
        ],
        "affirmations": [
            "I am doing my best, and my best is enough.",
            "This exam does not define my worth.",
            "I have survived every hard day so far.",
            "Progress, not perfection.",
            "One chapter at a time. One breath at a time.",
            "My mental health matters more than any grade.",
        ]
    }