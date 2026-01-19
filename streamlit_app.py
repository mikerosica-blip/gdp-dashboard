import streamlit as st
import google.generativeai as genai
import time

# 1. Page Layout (Wide and readable for Chromebooks)
st.set_page_config(page_title="6th Grade Editor", layout="wide")

# 2. Custom Styles (Big text for 6th graders)
st.markdown("""
    <style>
    .stTextArea textarea {font-size: 22px !important;}
    .stMarkdown p, .stMarkdown li { font-size: 24px !important; line-height: 1.4; }
    h3 { text-align: left !important; margin-top: 0 !important; }
    strong { color: #1E88E5; font-weight: 800; }
    u { text-decoration: underline; color: #D32F2F; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. Teacher Settings Storage
if 'guidance' not in st.session_state: st.session_state.guidance = ""

with st.sidebar:
    st.header("🔑 Access")
    pw = st.text_input("Teacher Password:", type="password")
    
    if pw == "writebetter": 
        st.divider()
        st.header("🍎 Teacher Controls")
        st.session_state.guidance = st.text_area("Guidance Instructions:", value=st.session_state.guidance)
        st.success("Admin Mode: Unlocked")
    else:
        st.info("Teacher settings are hidden.")

# 4. Your API Key (Moving to Paid Tier fixes the Error 429)
api_key = "AIzaSyBS2xMt2Po99bfstI9SRhe_asLH5ixULdE"

# 5. Main App Interface
col1, col2 = st.columns(2)

with col1:
    draft = st.text_area("Paste your writing here:", height=500, key="student_draft")
    
    # Buttons
    btn_col1, btn_col2 = st.columns([1, 4])
    with btn_col1:
        if st.button("Check My Draft"):
            if not draft:
                st.warning("Please paste your writing first!")
            else:
                try:
                    genai.configure(api_key=api_key)
                    # UPDATED: Using Gemini 2.5-Flash to fix the 404 error
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # Refined Classroom Prompt
                    prompt = f"""
                    You are a 6th grade writing editor. Use middle-school language. 
                    Start immediately with '### Suggestions:'.
                    LIMIT: Provide exactly 5-6 suggestions total.
                    KEYWORDS: Start every bullet with **<u>ADD</u>**, **<u>REMOVE</u>**, **<u>MOVE</u>**, **<u>SUBSTITUTE</u>**, or **<u>CORRECT</u>**.
                    CONTENT-BLIND: Do not discuss story topics.
                    
                    TEACHER GUIDANCE: {st.session_state.guidance}
                    
                    STUDENT DRAFT:
                    {draft}
                    """
                    
                    with st.spinner('Checking your work...'):
                        res = model.generate_content(prompt)
                        with col2:
                            st.markdown(res.text, unsafe_allow_html=True)
                except Exception as e:
                    if "429" in str(e):
                        st.error("Too many clicks! Wait 60 seconds.")
                    else:
                        st.error(f"Error: {e}")
    with btn_col2:
        if st.button("Reset Screen"):
            st.rerun()
