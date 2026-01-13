from firecrawl import Firecrawl
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

if "api" not in st.session_state:
    st.session_state.api = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

firecrawl = st.session_state.api
 
schema = {
    "type": "object",
    "properties": {
        "university_name": {"type": "string"},
        "faculty_name":{"type":"string"},
        "programs": {
            "type": "array",
            "items": {"type": "string"}  
        }
    }
}

prompt = "Extract university name, faculty names and program names."


@st.cache_data(show_spinner=True)
def scrap_webpage(url):
    response = firecrawl.extract(
        urls=[url],
        prompt=prompt,
        schema=schema,
        enable_web_search=False,
    )
    data = response.data

    if isinstance(data, dict):
        data = [data]

    normalized_data = []

    for uni in data:
        if not isinstance(uni, dict):
            continue

        programs = uni.get("programs", [])

        if isinstance(programs, dict):
            programs = list(programs.values())
        elif not isinstance(programs, list):
            programs = []

        uni["programs"] = programs
        normalized_data.append(uni)

    st.write(normalized_data)
    return normalized_data


