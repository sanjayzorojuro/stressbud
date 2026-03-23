import streamlit as st
import requests
import uuid

# ─── CONFIG ──────────────────────────────────────────────────────────────────
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="StressBud 🌱", page_icon="🌱", layout="centered")

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f1117;
    color: #e0e0e0;
}

.stApp { background: #0f1117; }

/* Hero */
.hero-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}
.hero-subtitle {
    text-align: center;
    font-size: 1.05rem;
    color: #888;
    margin-bottom: 2rem;
}

/* All buttons — round pill style */
div.stButton > button {
    border-radius: 50px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1.5rem !important;
    border: 2px solid rgba(255,255,255,0.1) !important;
    background: linear-gradient(145deg, #1a1a2e, #16213e) !important;
    color: #e0e0e0 !important;
    transition: all 0.3s ease !important;
    min-height: 60px !important;
    width: 100% !important;
}
div.stButton > button:hover {
    border-color: rgba(67, 233, 123, 0.5) !important;
    box-shadow: 0 0 20px rgba(67, 233, 123, 0.15) !important;
    transform: translateY(-2px) !important;
    color: #fff !important;
}

/* SOS button override */
div[data-testid="stColumn"]:nth-child(2) div.stButton > button {
    background: linear-gradient(145deg, #8b0000, #cc0000, #ff1a1a) !important;
    border: 2px solid rgba(255, 60, 60, 0.6) !important;
    color: #fff !important;
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    min-height: 70px !important;
    animation: sos-pulse 2s ease-in-out infinite !important;
    box-shadow: 0 0 30px rgba(255, 0, 0, 0.3) !important;
}
div[data-testid="stColumn"]:nth-child(2) div.stButton > button:hover {
    animation: none !important;
    box-shadow: 0 0 40px rgba(255, 0, 0, 0.5) !important;
    transform: scale(1.03) !important;
}

@keyframes sos-pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(255,0,0,0.3); }
    50%       { box-shadow: 0 0 40px rgba(255,0,0,0.6); }
}

/* Helpline banner */
.helpline-banner {
    background: linear-gradient(145deg, #1a0000, #2d0a0a);
    border: 1px solid rgba(255, 60, 60, 0.3);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
}
.helpline-banner h3 { color: #ff6b6b; font-size: 1rem; margin-bottom: 0.75rem; }
.helpline-item {
    display: flex;
    justify-content: space-between;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.9rem;
}
.helpline-item:last-child { border-bottom: none; }
.helpline-name  { color: #e0e0e0; font-weight: 500; }
.helpline-number { color: #ff9999; font-weight: 700; letter-spacing: 0.5px; }

/* SOS header */
.sos-header {
    text-align: center;
    font-size: 1.8rem;
    font-weight: 800;
    color: #ff6b6b;
    margin-bottom: 0.2rem;
}
.sos-subheader {
    text-align: center;
    font-size: 1rem;
    color: #888;
    margin-bottom: 1.5rem;
}

/* Mode header */
.mode-header {
    text-align: center;
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #43e97b, #38f9d7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.mode-subheader {
    text-align: center;
    font-size: 1rem;
    color: #888;
    margin-bottom: 1.5rem;
}

/* Chat messages */
.stChatMessage { border-radius: 16px !important; }
[data-testid="stChatMessageContent"] { color: #e0e0e0 !important; }

/* Back button */
div.stButton.back > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #888 !important;
    min-height: 40px !important;
    font-size: 0.9rem !important;
    width: auto !important;
    padding: 0.4rem 1.2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "mode"            not in st.session_state: st.session_state.mode = "home"
if "messages"        not in st.session_state: st.session_state.messages = []
if "sos_messages"    not in st.session_state: st.session_state.sos_messages = []
if "sos_initialized" not in st.session_state: st.session_state.sos_initialized = False
if "session_id"      not in st.session_state: st.session_state.session_id = str(uuid.uuid4())

# ─── HELPER ───────────────────────────────────────────────────────────────────
def call_backend(message, history=[]):
    try:
        res = requests.post(
            f"{BACKEND_URL}/api/chat",
            json={"message": message, "session_id": st.session_state.session_id, "history": history},
            timeout=30
        )
        data = res.json()
        return data.get("reply", "I'm here for you 💙"), data.get("category", "general")
    except Exception as e:
        return f"❌ Backend error: {e}", "general"

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.mode == "home":
    st.markdown('<div class="hero-title">🌱 StressBud</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Your companion for exam season — mentor, friend, advisor.</div>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1.3, 1], gap="medium")
    with col1:
        if st.button("📚 Syllabus", key="btn_syllabus"):
            st.session_state.mode = "syllabus"
            st.rerun()
    with col2:
        if st.button("🚨 SOS", key="btn_sos"):
            st.session_state.mode = "sos"
            st.session_state.sos_initialized = False
            st.rerun()
    with col3:
        if st.button("💪 Pressure", key="btn_pressure"):
            st.session_state.mode = "pressure"
            st.rerun()

    st.markdown("---")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Chat with StressBud..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
        reply, _ = call_backend(prompt, history)

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ══════════════════════════════════════════════════════════════════════════════
# SOS MODE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "sos":
    if st.button("← Back", key="btn_back_sos"):
        st.session_state.mode = "home"
        st.session_state.sos_messages = []
        st.session_state.sos_initialized = False
        st.rerun()

    st.markdown('<div class="sos-header">🚨 SOS — You\'re Safe Here</div>', unsafe_allow_html=True)
    st.markdown('<div class="sos-subheader">Take a breath. You\'re not alone. Let\'s talk.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="helpline-banner">
        <h3>📞 Crisis Helplines (India)</h3>
        <div class="helpline-item">
            <span class="helpline-name">iCall (Mon-Sat, 9am-9pm)</span>
            <span class="helpline-number">9152987821</span>
        </div>
        <div class="helpline-item">
            <span class="helpline-name">Vandrevala Foundation (24/7)</span>
            <span class="helpline-number">1860-2662-345</span>
        </div>
        <div class="helpline-item">
            <span class="helpline-name">AASRA (24/7)</span>
            <span class="helpline-number">9820466726</span>
        </div>
        <div class="helpline-item">
            <span class="helpline-name">Emergency</span>
            <span class="helpline-number">112</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Auto greeting
    if not st.session_state.sos_initialized:
        with st.spinner("Connecting..."):
            reply, _ = call_backend(
                "SOS mode activated. The user is in crisis. Greet them warmly, ask what's going on, and offer a breathing exercise.",
                []
            )
        st.session_state.sos_messages.append({"role": "assistant", "content": reply})
        st.session_state.sos_initialized = True

    for msg in st.session_state.sos_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("I'm here. Talk to me..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.sos_messages.append({"role": "user", "content": prompt})

        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.sos_messages[:-1]]
        reply, _ = call_backend(prompt, history)

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.sos_messages.append({"role": "assistant", "content": reply})

# ══════════════════════════════════════════════════════════════════════════════
# SYLLABUS MODE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "syllabus":
    if st.button("← Back", key="btn_back_syllabus"):
        st.session_state.mode = "home"
        st.rerun()

    st.markdown('<div class="mode-header">📚 Syllabus Help</div>', unsafe_allow_html=True)
    st.markdown('<div class="mode-subheader">Let\'s make a plan and tackle it together.</div>', unsafe_allow_html=True)

    if "syllabus_messages" not in st.session_state:
        st.session_state.syllabus_messages = []
        reply, _ = call_backend("Syllabus mode. Student needs help with exam prep and pending syllabus. Greet them and ask what subject or topic they're stuck on.", [])
        st.session_state.syllabus_messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.syllabus_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Tell me what you need help with..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.syllabus_messages.append({"role": "user", "content": prompt})

        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.syllabus_messages[:-1]]
        reply, _ = call_backend(prompt, history)

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.syllabus_messages.append({"role": "assistant", "content": reply})

# ══════════════════════════════════════════════════════════════════════════════
# PRESSURE MODE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.mode == "pressure":
    if st.button("← Back", key="btn_back_pressure"):
        st.session_state.mode = "home"
        st.rerun()

    st.markdown('<div class="mode-header">💪 Pressure Support</div>', unsafe_allow_html=True)
    st.markdown('<div class="mode-subheader">Family, peers, expectations — let\'s talk it out.</div>', unsafe_allow_html=True)

    if "pressure_messages" not in st.session_state:
        st.session_state.pressure_messages = []
        reply, _ = call_backend("Pressure mode. Student is feeling pressure from family, peers or college. Greet them warmly and ask what kind of pressure they're dealing with.", [])
        st.session_state.pressure_messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.pressure_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Tell me what's weighing on you..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.pressure_messages.append({"role": "user", "content": prompt})

        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.pressure_messages[:-1]]
        reply, _ = call_backend(prompt, history)

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.pressure_messages.append({"role": "assistant", "content": reply})