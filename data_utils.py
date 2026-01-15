def prepare_documents(scraped_data):
    documents = []
        # Normalize input: dict → list[dict]
    if isinstance(scraped_data, dict):
        scraped_data = [scraped_data]
    if not scraped_data or not isinstance(scraped_data, list):
        return documents


    for uni in scraped_data:
        if not isinstance(uni, dict):
             continue
        university = uni.get("university_name")
        faculty = uni.get("faculty_name")
        programs = uni.get("programs")
        if not university and not faculty and not programs:
            continue
        programs = programs if isinstance(programs, list) else []

        # ---- University-level document ----
        if programs:
            programs_text = "\n".join(f"- {p}" for p in programs)
        else:
            programs_text = "No program information available."

        documents.append(
            f"""
            University: {university or "Unknown"}
            Faculty: {faculty or "Unknown"}
            Programs Offered:{programs_text}""".strip()
        )

        # ---- Program-level documents ----
        for program in programs:
            documents.append(
                f"University: {university or 'Unknown'}\n"
                f"Faculty: {faculty or 'Unknown'}\n"
                f"Program: {program}"
            )

    return documents