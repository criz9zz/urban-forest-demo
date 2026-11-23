"""Sample FAQ chatbot demo (Streamlit + Google Gemini).

Everything the bot knows comes from faq.md. To reuse this for another
business, change BUSINESS_NAME / PHONE below and replace faq.md.
"""
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types

BUSINESS_NAME = "Urban Forest Cafe"
PHONE = "+91 87145 99228"
QUICK_QUESTIONS = [
    "What time do you open and close?",
    "Where are you located? Is there parking?",
    "Do you have vegetarian options?",
    "Can I book a table for a group?",
]

st.set_page_config(page_title=f"{BUSINESS_NAME} Assistant", page_icon="🌿")


def get_secret(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


API_KEY = get_secret("GEMINI_API_KEY")
MODEL = get_secret("GEMINI_MODEL", "gemini-3.5-flash")
BUSINESS_INFO = (Path(__file__).parent / "faq.md").read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""You are the friendly chat assistant for {BUSINESS_NAME}, a cafe in Kochi, Kerala.

Rules:
- Answer ONLY using the BUSINESS INFO below. Never invent prices, offers, dishes, timings or availability.
- If the answer is not in the info, say you don't have that detail and suggest calling {PHONE}.
- You cannot take bookings or orders. For bookings, tell the customer to call {PHONE}.
- For allergy or health questions, tell the customer to confirm with the staff.
- Keep answers short (1 to 3 sentences) and warm. Reply in the customer's language (English, Malayalam or Manglish).

BUSINESS INFO:
{BUSINESS_INFO}
"""


@st.cache_resource
def get_client():
    return genai.Client(api_key=API_KEY)


def ask_gemini(history: list[dict]) -> str:
    contents = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in history[-10:]  # keep only recent turns
    ]
    response = get_client().models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.3),
    )
    return (response.text or "").strip() or f"Sorry, please call us on {PHONE}."


st.title(f"🌿 {BUSINESS_NAME}")
st.caption("Sample demo built by Noufal. Details are to be confirmed by the cafe.")

if not API_KEY:
    st.error("Missing GEMINI_API_KEY. Add it in Streamlit secrets (see README).")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hi! 👋 Welcome to {BUSINESS_NAME}. Ask me about our timings, menu, location or bookings."}
    ]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# One-tap questions (handy for customers scanning the QR code)
quick = None
cols = st.columns(2)
for i, q in enumerate(QUICK_QUESTIONS):
    if cols[i % 2].button(q, key=f"quick{i}", use_container_width=True):
        quick = q

typed = st.chat_input("Type your question...")
prompt = (quick or typed or "").strip()[:300]

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
                        try:
                reply = ask_gemini(st.session_state.messages)
            except Exception as e:
                st.error(f"Debug: {e}")
                reply = f"Sorry, I'm having trouble right now. Please call us on {PHONE}."
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
