import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()

def chatbot(scrapped_data):
    if not scrapped_data:
        st.warning("No scraped data provided!")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        if "client" not in st.session_state:
            st.session_state.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        client = st.session_state.client

        system_prompt = f"""
You are a university and course advisor.

You MUST answer strictly using the scraped data below.
If the answer is not present, say "This information is not available."

Scraped Data:
{scrapped_data}

Rules:
- Do not hallucinate
- Do not use outside knowledge
- Be concise and accurate
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=420
        )

        reply = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply})

        return reply
