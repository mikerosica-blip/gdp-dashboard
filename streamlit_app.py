import streamlit as st
import google.generativeai as genai
import os

# 1. Page Layout (Optimized for 6th Grade Chromebooks)
st.set_page_config(page_title="6th Grade Editor", layout="wide")

# 2. Custom Styles (Matches the bold red feedback from your successful test)
st.markdown("""
    <style>
    .stTextArea textarea {font-size: 22px !important;}
    .stMarkdown p, .stMarkdown li { font-size: 24px !important; line-height: 1.5; }
    h3 { text-align: left !important; margin-top: 0 !important; }
    /* Formatting for the specific keywords you liked */
    strong { color: #D32F2F; font-weight: 800; text-decoration: underline; }
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

# 4. API Key (Pulls safely from your 'GEMINI_API_KEY' Secret)
api_key = os.environ.get("GEMINI_API_KEY")

# 5. Main App Interface
col1, col2 = st.columns(2)

with col1:
    draft = st.text_area("Paste your writing here:", height=500, key="student_draft")
    
    if st.button("Check My Draft"):
        if not draft:
            st.warning("Please paste your writing first!")
        elif not api_key:
            st.error("API Key not found! Please ensure you added GEMINI_API_KEY to GitHub Secrets.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Prompt designed to produce exactly 5-6 bullet points with your keywords
                prompt = f"""
                You are a 6th grade writing editor. Use middle-school language.  
                Start immediately with '### Suggestions:'.
                LIMIT: Provide exactly 5-6 suggestions total.
                KEYWORDS: Start every bullet with **ADD**, **REMOVE**, **MOVE**, **SUBSTITUTE**, or **CORRECT** in all caps.
                
                TEACHER GUIDANCE: {st.session_state.guidance}
                
                STUDENT DRAFT:
                {draft}
                """
                
                with st.spinner('Checking your work...'):
                    res = model.generate_content(prompt)
                    with col2:
                        st.write("### Suggestions (Click icon to copy):")
                        # This 'code' block provides the automatic copy button for your grading
                        st.code(res.text, language=None)
                        # This displays the pretty version for the student
                        st.markdown(res.text, unsafe_allow_html=True)
            except Exception as e:
                if "429" in str(e):
                    st.error("Too many clicks! Wait 60 seconds or click 'Upgrade' in Google Cloud.")
                else:
                    st.error(f"Error: {e}")
