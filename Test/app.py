import streamlit as st
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR=os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
from LLM_MODEL.llm import init_model, send_message
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI CHATBOT",page_icon="🤖", layout="centered")
st.title("🤖 Pro Chatbot")
st.caption("Created by Pradeepkumar")

PROVIDERS = [
    "OpenAI",
    "Gemini",
    "Ollama - Mistral",
    "Ollama - llama3",
]

with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("Select model provider", PROVIDERS)
    if st.button("Clear conversation"):
        st.session_state.history = []

if "history" not in st.session_state:
    st.session_state.history = []

def render_history():
    for role, text in st.session_state.history:
        if role == "User":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**Assistant:** {text}")

messages_container = st.container()

with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_area("Message", height=140, key="input")
    submitted = st.form_submit_button("Send")
    if submitted:
        if user_input and user_input.strip():
            st.session_state.history.append(("User", user_input))
            cfg = init_model(provider)
            with st.spinner("Waiting for response..."):
                reply = send_message(cfg, user_input, history=st.session_state.history)
            st.session_state.history.append(("Assistant", reply))

with messages_container:
    st.subheader("Conversation")
    render_history()


# To run this app, use the command:
# streamlit run ./Test/app.py --server.port 8505 --server.address localhost