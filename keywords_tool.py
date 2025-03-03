import streamlit as st
import re
from searching import process_keywords

def run(client):
    # Main interface for keyword processing (only accessible if credentials are uploaded)
    st.write("This tool searches Google for keywords. The results are saved [here](https://docs.google.com/spreadsheets/d/1D6biQSBhLQ_qDqZnUQfWFUjJjiuUmuiM9n7CLDQrNiI/).")

    # Language options and descriptions
    language_options = {
        "Arabic (ar)": "ar",
        "English (en)": "en",
        "Hebrew (he)": "he"
    }

    region_options = {
        "Israel (il)": "il",
        "Palestinian (ps)": "ps"
    }

    engine_options = {
        "Pip Library": "library",
        "API Service": "API",
    }

    # Inputs for Keywords Search
    with st.form("keywords_search_form"):
        # Keywords input
        keywords_query = st.text_area("Keywords List:",
        help="Enter the keywords you want to search for. Use commas to separate multiple keywords.")
        
        # Language and Max Results in the same row
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_language = st.selectbox(
                "Language:",
                options=list(language_options.keys()),
                help="Choose the language for the google search."
            )
            language = language_options[selected_language]  
        with col2:
            selected_region = st.selectbox(
                "Region:",
                options=list(region_options.keys()),
                help="Choose the region for the google search."
            )
            region = region_options[selected_region]  
        with col3:
            limit = st.selectbox(
                "Max Results:",
                options=[100, 50, 10],
                index=0,
                help="Choose the max number of results to retrieve."
            )

        # Include inurl and homepage only in the same row
        col3, col4 = st.columns(2)
        with col3:
            include_inurl = st.checkbox(
                "Include 'inurl' in the search",
                value=False,
                help="Check this box if you want to include 'inurl' in the search results."
            )
        with col4:
            homepage_only = st.checkbox(
                "Include only homepage results",
                value=False,
                help="Check this box if you want to search only for pages that are homepages (domain or subdomain)."
            )

        selected_engine = st.selectbox("Engine:",
        options=list(engine_options.keys()), help="Choose the search engine technology.")
        engine = engine_options[selected_engine]
        
        # Submit button
        submit_button = st.form_submit_button("Search")

    # Handle form submission
    if submit_button:
        # Validate inputs
        if not keywords_query:
            st.error("Please provide at least one keyword.")
        else:
            keywords_query = re.split(r"[,\n]", keywords_query) # Split by commas and linebreaks
            keywords_query = [kw.strip() for kw in keywords_query if kw.strip()]  # Remove extra spaces and ignore empty strings

            st.write(f"**Keywords List:** {keywords_query} | **Language:** {language} | **Region:** {region} | **Number of Results:** {limit} | **Include 'inurl':** {'Yes' if include_inurl else 'No'} | **Homapage only:** {'Yes' if homepage_only else 'No'}")

            # Call the process_keywords function with the selected limit
            sheet_id = st.secrets["google_id"]
            process_keywords(client, sheet_id, keywords_query, lang=language, inurl=include_inurl, limit=limit, homepage=homepage_only, engine=engine, country=region)
            st.info("The URLs were added to the file.")
