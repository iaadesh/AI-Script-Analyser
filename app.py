import os
import sys

# Ensure project root is on the path when running `streamlit run app.py`
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from config.settings import settings
from core.analyzer import analyze_script
from ui.components import render_header, render_analysis

# ---------------------------------------------------------------------------
# Page config — must be the very first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=settings.app_title,
    page_icon=settings.app_icon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Global dark-mode CSS overrides
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp { background-color: #0a0a0f; color: #e8e8f0; }
        .block-container { max-width: 900px; padding-top: 1rem; }

        .stTextArea textarea {
            background-color: #111118 !important;
            color: #e8e8f0 !important;
            border: 1px solid #2a2a3a !important;
            border-radius: 10px !important;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
        }

        .stButton > button {
            background: linear-gradient(135deg, #6d28d9, #4f46e5);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 2rem;
            font-weight: 700;
            font-size: 1rem;
            width: 100%;
            transition: opacity 0.2s;
        }
        .stButton > button:hover { opacity: 0.88; }

        hr { border-color: #1e1e2e !important; }
        .stAlert { border-radius: 10px; }
        .streamlit-expanderHeader {
            background: #111118 !important;
            border-radius: 8px !important;
        }

        /* Hide sidebar toggle entirely */
        [data-testid="collapsedControl"] { display: none; }

        .stCaption { color: #888 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------
render_header()

EXAMPLE_SCRIPT = """Title: The Last Message

Scene
Riya receives a message from her ex-boyfriend after five years.

Dialogue
Riya: Why now?
Arjun: Because today I learned the truth.
Riya: What truth?
Arjun: That the accident wasn't your fault.
Riya: (long silence) You knew all along?
Arjun: No. But someone did.
Riya: Who?
Arjun: The one person you trusted most.
"""

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("#### 📄 Paste Your Script")
with col2:
    if st.button("Load Example", use_container_width=True):
        st.session_state["script_input"] = EXAMPLE_SCRIPT

script_text = st.text_area(
    label="Script Input",
    value=st.session_state.get("script_input", ""),
    placeholder="Paste your script here...\n\nTitle: Your Script Title\n\nScene\nDescribe the setting...\n\nDialogue\nCharacter: Line...",
    height=280,
    max_chars=settings.max_script_length,
    label_visibility="collapsed",
    key="script_input",
)

char_count = len(script_text)
st.caption(f"{char_count:,} / {settings.max_script_length:,} characters")

st.markdown("<br/>", unsafe_allow_html=True)
analyze_btn = st.button("🔍 Analyze Script", use_container_width=False)

# ---------------------------------------------------------------------------
# Analysis execution
# ---------------------------------------------------------------------------
if analyze_btn:
    if not script_text.strip():
        st.warning("Please paste a script before analyzing.")
    elif not settings.google_api_key:
        st.error("No Google API key found. Please set GOOGLE_API_KEY in your `.env` file.")
    else:
        with st.spinner("Analyzing your script with Gemini..."):
            try:
                analysis = analyze_script(script_text)
                st.session_state["last_analysis"] = analysis
                st.success("Analysis complete!")
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.exception(e)

# Show last analysis if available (persists across reruns)
if "last_analysis" in st.session_state:
    st.markdown("<br/>", unsafe_allow_html=True)
    render_analysis(st.session_state["last_analysis"])