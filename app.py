import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/chat"
SOS_API_URL = "http://127.0.0.1:8000/api/sos-chat"

st.set_page_config(page_title="StressBud", page_icon="🌱", layout="centered")

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Hero section */
    .hero-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #b0b0b0;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }

    /* Button row container */
    .btn-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1.5rem;
        margin: 2rem 0;
    }

    /* Side buttons */
    div[data-testid="stColumn"]:nth-child(1) button,
    div[data-testid="stColumn"]:nth-child(3) button {
        width: 100%;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 16px;
        border: 2px solid rgba(255,255,255,0.1);
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        color: #e0e0e0;
        cursor: pointer;
        transition: all 0.3s ease;
        min-height: 80px;
    }
    div[data-testid="stColumn"]:nth-child(1) button:hover,
    div[data-testid="stColumn"]:nth-child(3) button:hover {
        border-color: rgba(67, 233, 123, 0.5);
        box-shadow: 0 0 20px rgba(67, 233, 123, 0.15);
        transform: translateY(-2px);
    }

    /* SOS Button */
    div[data-testid="stColumn"]:nth-child(2) button {
        width: 100%;
        padding: 1.25rem 2rem;
        font-size: 1.4rem;
        font-weight: 800;
        border-radius: 20px;
        border: 3px solid rgba(255, 60, 60, 0.6);
        background: linear-gradient(145deg, #8b0000, #cc0000, #ff1a1a);
        color: #ffffff;
        cursor: pointer;
        animation: sos-pulse 2s ease-in-out infinite;
        min-height: 100px;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.3), 0 0 60px rgba(255, 0, 0, 0.1);
    }
    div[data-testid="stColumn"]:nth-child(2) button:hover {
        animation: none;
        box-shadow: 0 0 40px rgba(255, 0, 0, 0.5), 0 0 80px rgba(255, 0, 0, 0.2);
        transform: scale(1.03);
        border-color: rgba(255, 100, 100, 0.8);
    }

    @keyframes sos-pulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.3), 0 0 40px rgba(255, 0, 0, 0.1);
        }
        50% {
            box-shadow: 0 0 40px rgba(255, 0, 0, 0.6), 0 0 80px rgba(255, 0, 0, 0.3);
        }
    }

    /* Helpline banner */
    .helpline-banner {
        background: linear-gradient(145deg, #1a0000, #2d0a0a);
        border: 1px solid rgba(255, 60, 60, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .helpline-banner h3 {
        color: #ff6b6b;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
        font-weight: 700;
    }
    .helpline-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.95rem;
    }
    .helpline-item:last-child {
        border-bottom: none;
    }
    .helpline-name {
        color: #e0e0e0;
        font-weight: 500;
    }
    .helpline-number {
        color: #ff9999;
        font-weight: 700;
        font-family: 'Inter', monospace;
        letter-spacing: 0.5px;
    }

    /* Back button */
    .back-btn button {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: #b0b0b0 !important;
        border-radius: 12px !important;
        padding: 0.5rem 1.25rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .back-btn button:hover {
        border-color: rgba(255,255,255,0.3) !important;
        color: #ffffff !important;
    }

    /* SOS mode header */
    .sos-header {
        text-align: center;
        font-size: 1.8rem;
        font-weight: 800;
        color: #ff6b6b;
        margin-bottom: 0.25rem;
    }
    .sos-subheader {
        text-align: center;
        font-size: 1rem;
        color: #999;
        margin-bottom: 1.5rem;
    }

    /* Chat message styling */
    .stChatMessage {
        border-radius: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if "mode" not in st.session_state:
    st.session_state.mode = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sos_messages" not in st.session_state:
    st.session_state.sos_messages = []
if "sos_initialized" not in st.session_state:
    st.session_state.sos_initialized = False

# ─── HOME / Landing Page ─────────────────────────────────────────────────────
if st.session_state.mode == "home":
    st.markdown('<div class="hero-title">🌱 StressBud</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Your companion for exam season : mentor, friend, therapist, advisor.</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1.3, 1], gap="medium")

    with col1:
        if st.button("📚 Syllabus", use_container_width=True, key="btn_syllabus"):
            st.toast("🚧 Syllabus mode coming soon!", icon="📚")

    with col2:
        if st.button("🚨 SOS", use_container_width=True, key="btn_sos"):
            st.session_state.mode = "sos"
            st.session_state.sos_initialized = False
            st.rerun()

    with col3:
        if st.button("💪 Pressure", use_container_width=True, key="btn_pressure"):
            st.toast("🚧 Pressure mode coming soon!", icon="💪")

    st.markdown("---")
    

    # Display standard chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for custom prompts
    if prompt := st.chat_input("Chat with StressBud"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            response = requests.post(API_URL, json={"message": prompt})
            reply = response.json().get("reply", "Something went wrong.") if response.status_code == 200 else f"Error: {response.status_code}"
        except Exception as e:
            reply = f"Error connecting to backend: {e}"

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ─── SOS Mode ────────────────────────────────────────────────────────────────
elif st.session_state.mode == "sos":

    # Back button
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="btn_back"):
        st.session_state.mode = "home"
        st.session_state.sos_messages = []
        st.session_state.sos_initialized = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # SOS Header
    st.markdown('<div class="sos-header">🚨 SOS — You\'re Safe Here</div>', unsafe_allow_html=True)
    st.markdown('<div class="sos-subheader">Take a breath. You\'re not alone. Let\'s talk.</div>', unsafe_allow_html=True)

    # Helpline banner
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
            <span class="helpline-name">Snehi</span>
            <span class="helpline-number">044-24640050</span>
        </div>
        <div class="helpline-item">
            <span class="helpline-name">Emergency</span>
            <span class="helpline-number">112</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Auto-send initial SOS context to get the AI's first response
    if not st.session_state.sos_initialized:
        init_message = (
            "[SOS MODE ACTIVATED] The user has just pressed the emergency SOS button. "
            "They may be experiencing a crisis — depression, suicidal thoughts, or a panic attack. "
            "Please greet them warmly and gently. Ask them what's going on. Offer an immediate breathing exercise."
        )
        try:
            response = requests.post(SOS_API_URL, json={"message": init_message})
            reply = response.json().get("reply", "I'm here for you. Tell me what's on your mind. 💙") if response.status_code == 200 else "I'm here for you. Tell me what's on your mind. 💙"
        except Exception:
            reply = "I'm here for you. You're not alone. Take a slow breath with me. Tell me what's going on. 💙"

        st.session_state.sos_messages.append({"role": "assistant", "content": reply})
        st.session_state.sos_initialized = True

    # Display SOS chat history
    for message in st.session_state.sos_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # SOS Chat input
    if prompt := st.chat_input("I'm here. Talk to me..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.sos_messages.append({"role": "user", "content": prompt})

        try:
            response = requests.post(SOS_API_URL, json={"message": prompt})
            reply = response.json().get("reply", "I'm still here with you. 💙") if response.status_code == 200 else f"Error: {response.status_code}"
        except Exception:
            reply = "I'm having trouble connecting right now, but please know — you are not alone. If you're in crisis, please call one of the helplines above. 💙"

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.sos_messages.append({"role": "assistant", "content": reply})
