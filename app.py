import streamlit as st
import requests
from firebase_auth_component import firebase_auth_button

API_URL = "http://127.0.0.1:8000/api/chat"
SOS_API_URL = "http://127.0.0.1:8000/api/sos-chat"

st.set_page_config(page_title="StressBud", page_icon="🌱", layout="centered")

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

    .stApp {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── NAV BAR ── */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.25rem 0 1.5rem 0;
        margin-bottom: 0.5rem;
    }
    .nav-logo {
        font-family: 'DM Serif Display', serif;
        font-size: 1.4rem;
        color: #d4f5c4;
        letter-spacing: -0.3px;
    }

    /* ── HERO ── */
    .hero-wrap {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }
    .hero-eyebrow {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #6ee27a;
        background: rgba(110, 226, 122, 0.08);
        border: 1px solid rgba(110, 226, 122, 0.2);
        padding: 0.3rem 0.9rem;
        border-radius: 100px;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 3.6rem;
        line-height: 1.1;
        color: #f0f4f0;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    .hero-title em {
        font-style: italic;
        color: #6ee27a;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: #7a8f7a;
        max-width: 400px;
        margin: 0 auto 2.5rem auto;
        line-height: 1.65;
        font-weight: 400;
    }

    /* ── LOGIN BUTTON (nav) ── */
    .nav-login-btn button {
        background: transparent !important;
        border: 1px solid rgba(110, 226, 122, 0.35) !important;
        color: #6ee27a !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 1.1rem !important;
        border-radius: 100px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.2px !important;
        min-height: unset !important;
        height: auto !important;
        line-height: 1.4 !important;
    }
    .nav-login-btn button:hover {
        background: rgba(110, 226, 122, 0.08) !important;
        border-color: rgba(110, 226, 122, 0.6) !important;
    }

    /* ── USER PILL (when logged in) ── */
    .user-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(110, 226, 122, 0.07);
        border: 1px solid rgba(110, 226, 122, 0.2);
        border-radius: 100px;
        padding: 0.3rem 0.8rem;
        font-size: 0.85rem;
        color: #a8d5a8;
        font-weight: 500;
    }
    .user-dot {
        width: 7px; height: 7px;
        background: #6ee27a;
        border-radius: 50%;
        display: inline-block;
    }

    /* sign-out link */
    .signout-btn button {
        background: transparent !important;
        border: none !important;
        color: #556655 !important;
        font-size: 0.78rem !important;
        font-weight: 400 !important;
        padding: 0 !important;
        min-height: unset !important;
        height: auto !important;
        text-decoration: underline !important;
        cursor: pointer !important;
    }
    .signout-btn button:hover { color: #6ee27a !important; }

    /* ── FEATURE CARDS ── */
    div[data-testid="stColumn"]:nth-child(1) button,
    div[data-testid="stColumn"]:nth-child(2) button,
    div[data-testid="stColumn"]:nth-child(3) button {
        width: 100%;
        height: 110px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.07) !important;
        background: rgba(255,255,255,0.03) !important;
        color: #c8d8c8 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.25s ease !important;
        letter-spacing: -0.1px !important;
    }
    div[data-testid="stColumn"]:nth-child(1) button:hover,
    div[data-testid="stColumn"]:nth-child(3) button:hover {
        border-color: rgba(110, 226, 122, 0.25) !important;
        background: rgba(110, 226, 122, 0.05) !important;
        transform: translateY(-2px) !important;
    }

    /* SOS card override */
    div[data-testid="stColumn"]:nth-child(2) button {
        border-color: rgba(255, 80, 80, 0.25) !important;
        background: rgba(255, 60, 60, 0.04) !important;
        color: #f5a0a0 !important;
        animation: sos-breathe 3s ease-in-out infinite !important;
    }
    div[data-testid="stColumn"]:nth-child(2) button:hover {
        border-color: rgba(255, 80, 80, 0.5) !important;
        background: rgba(255, 60, 60, 0.08) !important;
        animation: none !important;
        transform: translateY(-2px) !important;
    }
    @keyframes sos-breathe {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255,60,60,0); }
        50% { box-shadow: 0 0 18px 2px rgba(255,60,60,0.12); }
    }

    /* ── DIVIDER ── */
    hr { border-color: rgba(255,255,255,0.06) !important; }

    /* ── SOS PAGE ── */
    .helpline-banner {
        background: rgba(255, 40, 40, 0.04);
        border: 1px solid rgba(255, 80, 80, 0.15);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    .helpline-banner h3 { color: #f08080; font-size: 0.9rem; margin-bottom: 0.75rem; font-weight: 600; letter-spacing: 0.3px; }
    .helpline-item {
        display: flex; justify-content: space-between; align-items: center;
        padding: 0.45rem 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 0.9rem;
    }
    .helpline-item:last-child { border-bottom: none; }
    .helpline-name { color: #b0bfb0; font-weight: 400; }
    .helpline-number { color: #f5a0a0; font-weight: 600; font-family: 'DM Sans', monospace; letter-spacing: 0.5px; }

    .sos-header { text-align: center; font-family: 'DM Serif Display', serif; font-size: 2rem; color: #f08080; margin-bottom: 0.2rem; font-weight: 400; }
    .sos-subheader { text-align: center; font-size: 0.95rem; color: #6a7a6a; margin-bottom: 1.5rem; }

    /* ── BACK BUTTON ── */
    .back-btn button {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #6a7a6a !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        min-height: unset !important;
        height: auto !important;
        padding: 0.4rem 1rem !important;
    }
    .back-btn button:hover { color: #c8d8c8 !important; border-color: rgba(255,255,255,0.2) !important; }

    /* ── LOGIN PAGE ── */
    .login-page-wrap {
        max-width: 380px;
        margin: 3rem auto 0 auto;
        text-align: center;
    }
    .login-page-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.2rem;
        color: #f0f4f0;
        margin-bottom: 0.4rem;
        font-weight: 400;
    }
    .login-page-sub {
        font-size: 0.92rem;
        color: #6a7a6a;
        margin-bottom: 2rem;
        line-height: 1.55;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
for key, val in {
    "mode": "home",
    "messages": [],
    "sos_messages": [],
    "sos_initialized": False,
    "user": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ══════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════
if st.session_state.mode == "home":

    # ── NAV ──
    col_logo, col_spacer, col_auth = st.columns([3, 3, 1.5])
    with col_logo:
        st.markdown('<div class="nav-logo">🌱 StressBud</div>', unsafe_allow_html=True)
    with col_auth:
        if st.session_state.user is None:
            st.markdown('<div class="nav-login-btn">', unsafe_allow_html=True)
            if st.button("Login", key="btn_nav_login"):
                st.session_state.mode = "login"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            name = st.session_state.user.get("displayName", "User")
            st.markdown(f'<div class="user-pill"><span class="user-dot"></span>{name}</div>', unsafe_allow_html=True)
            st.markdown('<div class="signout-btn">', unsafe_allow_html=True)
            if st.button("sign out", key="btn_signout"):
                st.session_state.user = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── HERO ──
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-eyebrow">Exam season companion</div>
        <div class="hero-title">Calm through<br><em>every storm.</em></div>
        <div class="hero-sub">Your mentor, friend, therapist, and advisor — all in one place, whenever you need it.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── FEATURE CARDS ──
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        if st.button("📚\nSyllabus", use_container_width=True, key="btn_syllabus"):
            st.toast("📚 Syllabus mode coming soon!")
    with col2:
        if st.button("🚨\nSOS", use_container_width=True, key="btn_sos"):
            st.session_state.mode = "sos"
            st.session_state.sos_initialized = False
            st.rerun()
    with col3:
        if st.button("💪\nPressure", use_container_width=True, key="btn_pressure"):
            st.toast("💪 Pressure mode coming soon!")

    st.markdown("---")

    # ── CHAT ──
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Chat with StressBud…"):
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


# ══════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════
elif st.session_state.mode == "login":

    # Back button
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Back", key="btn_back_login"):
        st.session_state.mode = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="login-page-wrap">
        <div class="login-page-title">Welcome back.</div>
        <div class="login-page-sub">Sign in to save your chats and personalise your experience.</div>
    </div>
    """, unsafe_allow_html=True)

    # The full-page auth component
    user_data = firebase_auth_button(key="login_page_auth")
    if user_data:
        st.session_state.user = user_data
        st.session_state.mode = "home"
        st.rerun()


# ══════════════════════════════════════════════════════
# SOS PAGE
# ══════════════════════════════════════════════════════
elif st.session_state.mode == "sos":

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="btn_back_sos"):
        st.session_state.mode = "home"
        st.session_state.sos_messages = []
        st.session_state.sos_initialized = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sos-header">🚨 You\'re Safe Here</div>', unsafe_allow_html=True)
    st.markdown('<div class="sos-subheader">Take a breath. You\'re not alone. Let\'s talk.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="helpline-banner">
        <h3>📞 Crisis Helplines (India)</h3>
        <div class="helpline-item">
            <span class="helpline-name">iCall (Mon–Sat, 9am–9pm)</span>
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

    for message in st.session_state.sos_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("I'm here. Talk to me…"):
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