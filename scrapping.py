from firecrawl import Firecrawl
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


@st.cache_data
def scrape_universities():
    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

    schema = {
        "type": "object",
        "properties": {
            "university_name": {"type": "string"},
            "courses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "course_name": {"type": "string"},
                        "general_details": {"type": "string"},
                    },
                },
            },
        },
    }

    prompt = """
    Extract the university name and all academic programs,
    with course name and general details. Do not repeat a course name from one university.
    """

    urls = [
        "https://nust.edu.pk",
        "https://lums.edu.pk",
        "https://uet.edu.pk",
        "https://comsats.edu.pk",
        "https://uok.edu.pk",
        "https://itu.edu.pk",
        "https://nu.edu.pk",
        "https://pu.edu.pk",
        "https://giki.edu.pk",
        "https://iba.edu.pk",
    ]

    response = firecrawl.extract(
        urls=urls,
        prompt=prompt,
        schema=schema,
        enable_web_search=True,
    )

    return response.data


def scrapwebpage():
    data = scrape_universities()
    return data

