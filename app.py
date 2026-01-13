
import streamlit as st
from scrapping import scrap_webpage 

def main():
    st.title("University Course Bot")

    all_data = []
    urls = [
        "https://admissions.umt.edu.pk/search.aspx",
        "https://www.vu.edu.pk/StudyScheme/StudyScheme",
        "https://logix.edu.pk/course-detail/1/all-academic-programs-by-vu",
        "https://itu.edu.pk/academics/",
        "https://pu.edu.pk/program",
        "https://giki.edu.pk/Programs/",
        "https://ucp.edu.pk/undergraduate/",
        "https://ucp.edu.pk/postgraduate/",
        "https://nust.edu.pk/academics/"
    ]
    for url in urls:
        st.write(f"Scraping: {url} ...")
        data = scrap_webpage(url)
        st.write(data)
        all_data.append(data)

    st.success("Scraping completed!")

if __name__ == "__main__":
    main()
