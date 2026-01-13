
import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from scrapping import scrap_webpage
from data_utils import prepare_documents
from vector_db import ChromaVectorDB

load_dotenv()

st.set_page_config(page_title="University Course Advisor", layout="wide")
st.title("University Course Advisor Bot")

# --------------------------
# Session state init
# --------------------------
if "scraped_data" not in st.session_state:
    st.session_state.scraped_data = None

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "messages" not in st.session_state:
    st.session_state.messages = []

all_data = []
urls = [
        "https://www.vu.edu.pk/StudyScheme/StudyScheme",
        "https://itu.edu.pk/academics/",
    ]    
# --------------------------
# Load data button (IMPORTANT)
# --------------------------
st.subheader("Step 1: Load University Data")

if st.button("Load / Refresh University Data"):
    with st.spinner("Scraping university websites..."):
        try:
            vector_db = ChromaVectorDB()
            for url in urls:
                st.write(f"Scraping: {url} ...")
                data = scrap_webpage(url)
                all_data.extend(data) 
            if all_data:
                docs = prepare_documents(all_data)
                vector_db.add_documents(docs)
                st.session_state.vector_db = vector_db
                st.session_state.scraped_data = all_data
                st.success("University data loaded successfully.")
            else:
                st.error("No valid data scraped.")

            st.session_state.vector_db = vector_db
            st.session_state.scraped_data = all_data
        except Exception as e:
            st.error(f"Scraping failed: {e}")

# --------------------------
# Stop app if data not loaded
# --------------------------
if st.session_state.vector_db is None:
    st.info("Please load university data before asking questions.")
    st.stop()

# --------------------------
# Chat input
# --------------------------
st.subheader("Ask a Question")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask about universities or courses")
    submit = st.form_submit_button("Send")

# --------------------------
# Handle query
# --------------------------
if submit and user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Searching relevant information..."):
        relevant_docs = st.session_state.vector_db.query(
            user_input, top_k=5
        )
    context = "\n\n".join(
        [item if isinstance(item, str) else " ".join(item) for item in relevant_docs]
    ) if relevant_docs else ""


    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    if not GROQ_API_KEY:
        reply = context if context else "This information is not available."
    else:
        if "client" not in st.session_state:
            st.session_state.client = Groq(api_key=GROQ_API_KEY)

        system_prompt = f"""
You are a university course advisor.
Answer ONLY using the context below.
Provide exact university and course names.
If the course is not mentioned in the context, reply: "This information is not available."


Context:
{context}
"""

        response = st.session_state.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0.3,
            max_tokens=300,
        )

        reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
# --------------------------
# Display chat
# --------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Advisor:** {msg['content']}")