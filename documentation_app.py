import streamlit as st
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables from the .env file
load_dotenv()

# Import the custom CSS from the new style folder
from style.style import CUSTOM_CSS

# Import the agents and runner
from components.agents import Agent, Runner
from components.analyzer import document_analyzer
from components.enforcer import style_enforcer

# --- Page Configuration and CSS ---
st.set_page_config(
    page_title="Docu-Align Agent",
    page_icon="✍️",
    layout="wide"
)

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- Agent Initialization ---
# Check for the API key in the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("API key not found! Please add your OpenAI API key to the .env file.")
else:
    runner = Runner(api_key=openai_api_key)

# --- Main Application Layout ---
st.title("Docu-Align Agent")
st.markdown("A tool to analyze and improve your technical documentation using AI agents.")
st.divider()

# Input area for documentation content
st.header("Upload or Paste Documentation Content")
uploaded_file = st.file_uploader(
    "Upload the existing documentation file (TXT, MD, DOCX, PDF)",
    type=["txt", "md", "docx", "pdf"]
)

user_content = st.text_area(
    "Or paste the content directly below:",
    height=300,
    placeholder="e.g., A formal, technical manual for a software product..."
)

# Process the input content
content = ""
if uploaded_file:
    content = uploaded_file.getvalue().decode("utf-8")
elif user_content:
    content = user_content

# --- Agent Actions ---
st.divider()
st.header("Agent Actions")
success_message_placeholder = st.empty()

if st.button("Run Docu-Align Agents"):
    # Clear previous state
    st.session_state.pop("analysis_report", None)
    st.session_state.pop("final_document", None)
    st.session_state.pop("success", None)

    if not content:
        st.warning("Please provide content to analyze.")
    elif not openai_api_key:
        st.error("API key not found. Please check your `.env` file.")
    else:
        with st.spinner("Analyzing and enforcing style..."):
            try:
                # 1. Run the Document Analyzer
                loop = asyncio.new_event_loop()
                analysis_result = loop.run_until_complete(runner.run(document_analyzer, content))
                loop.close()
                st.session_state["analysis_report"] = analysis_result.final_output

                # 2. Prepare for handoff and run Style Enforcer
                handoff_prompt = f"""
                <original_content>
                {content}
                </original_content>

                <analysis_report>
                {st.session_state["analysis_report"]}
                </analysis_report>
                """
                loop = asyncio.new_event_loop()
                enforced_result = loop.run_until_complete(runner.run(style_enforcer, handoff_prompt))
                loop.close()
                st.session_state["final_document"] = enforced_result.final_output
                st.session_state["success"] = True

            except Exception as e:
                st.session_state["success"] = False
                st.error(f"An error occurred: {e}")

# Display final outputs
if "final_document" in st.session_state:
    if st.session_state.get("success"):
        success_message_placeholder.success("Analysis and Style Enforcement Complete!")
    
    st.subheader("Analysis Report")
    st.text_area(
        "Report from Document Analyzer",
        value=st.session_state["analysis_report"],
        height=200,
        disabled=True
    )
    
    st.subheader("Polished Document Draft")
    st.text_area(
        "Final Document from Style Enforcer",
        value=st.session_state["final_document"],
        height=400
    )
