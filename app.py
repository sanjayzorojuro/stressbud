import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/chat"

st.set_page_config(page_title="StressBud", page_icon="🌱", layout="centered")

st.title("🌱 StressBud")
st.markdown("Your friendly neighbourhood companion for exam season. A mentor, friend, therapist, and advisor all in one.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is on your mind?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = requests.post(API_URL, json={"message": prompt})
        reply = response.json().get("reply", "Something went wrong.") if response.status_code == 200 else f"Error: {response.status_code}"
    except Exception as e:
        reply = "Backend server is not running or unreachable. Please start the FastAPI backend first."

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
