import streamlit as st
import google.generativeai as genai

# 1. Page Layout
st.set_page_config(page_title="6th Grade Editor", layout="wide")

# 2. Custom Styles
st.markdown("""
    <style>
    .stTextArea textarea {font-size: 22px !important;}
    /* This makes the copyable code block look like regular text */
    code { font-size: 18px !important; color: #333 !important; background-color: #f9f9f9 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Teacher Settings
if 'guidance' not in st.session_state: st.session_state.guidance = ""

with st.sidebar:
    st.header("🔑 Access")
    pw = st.text_input("Teacher Password:", type="password")
    if pw == "writebetter": 
        st.divider()
        st.header("🍎 Teacher Controls")
        st.session_state.guidance = st.text_area("Guidance:", value=st.session_state.guidance)
    else:
        st.info("Teacher settings hidden.")

# 4. API Key (Ensure 'Upgrade' is clicked in Google Cloud!)
api_key = "AIzaSyBS2xMt2Po99bfstI9SRhe_asLH5ixULdE"

# 5. Main App
col1, col2 = st.columns(2)

with col1:
    draft = st.text_area("Paste your writing here:", height=500, key="student_draft")
    
    if st.button("Check My Draft"):
        if not draft:
            st.warning("Paste writing first!")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"6th grade editor. 5-6 bullets. Keywords: ADD, REMOVE, MOVE, SUBSTITUTE, CORRECT. Guidance: {st.session_state.guidance}. Draft: {draft}"
                
                with st.spinner('Checking...'):
                    res = model.generate_content(prompt)
                    with col2:
                        st.write("### Suggestions (Click icon to copy):")
                        # This 'code' block provides the automatic copy button
                        st.code(res.text, language=None)
            except Exception as e:
                if "429" in str(e):
                    st.error("Wait 60 seconds!")
                else:
                    st.error(f"Error: {e}")
