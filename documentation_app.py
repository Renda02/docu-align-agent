import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
from xml.etree import ElementTree as ET

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
    page_title="Docu-Align — AI-powered Documentation",
    page_icon="📝",
    layout="centered"
)

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
# Inject CSS to override default text area color
st.markdown("""
<style>
/* Target the text within disabled text areas to make it black */
textarea:disabled {
    -webkit-text-fill-color: black;
    color: black;
    opacity: 1; /* Ensure full opacity */
}
</style>
""", unsafe_allow_html=True)

# --- Navigation Header ---
st.markdown("""
<div class="nav-header">
    <div class="nav-container">
        <div class="nav-brand">
            <span class="nav-logo">📝</span>
            <span class="nav-title">DocuALIGN</span>
        </div>
        <div class="nav-links">
            <a href="#features" class="nav-link">Features</a>
            <a href="#pricing" class="nav-link">Pricing</a>
            <a href="#docs" class="nav-link">Docs</a>
            <a href="#signin" class="nav-link nav-signin">Sign In</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Agent Initialization ---
# Check for the API key in the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("⚠️ API key not found! Please add your OpenAI API key to the .env file.")
    st.stop()
else:
    runner = Runner(api_key=openai_api_key)

# --- Main Application Layout ---

# Modern headline with highlighted text
st.markdown(
    '<div class="headline">Transform your <span class="highlight">how-to guides</span> with AI-powered precision</div>',
    unsafe_allow_html=True
)

# Descriptive subtext
st.markdown(
    '<div class="subtext">Upload your draft how-to content and watch as our AI transforms it into a structured, professional guide following The Good Docs Project template standards.</div>',
    unsafe_allow_html=True
)

st.divider()

# --- Upload Section ---
st.markdown("## 📄 Upload Your Document")

# File uploader
uploaded_file = st.file_uploader(
    "Drop your document here",
    type=["txt", "md", "docx", "pdf"],
    help="Supported formats: .txt, .md, .docx, .pdf"
)

st.divider()

# Alternative text input
st.markdown("### ✏️ Or paste your content directly")

user_content = st.text_area(
    "Paste your how-to guide content here:",
    height=200,
    placeholder="Paste your how-to guide draft here...\n\nExample:\n# Setting up the development environment\n\n1. Download the installer\n2. Run the setup wizard\n3. Configure your API keys...",
    help="Paste any procedural or step-by-step content that you want to transform into a professional how-to guide"
)

# Process the input content
content = ""
if uploaded_file:
    try:
        content = uploaded_file.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        st.error("❌ Unable to decode file. Please ensure it's a text-based document.")
elif user_content:
    content = user_content

# --- Analysis Section ---
if content:
    st.divider()
    
    # Content preview
    with st.expander("📖 Content Preview", expanded=False):
        preview_text = content[:500] + "..." if len(content) > 500 else content
        st.text(preview_text)
        st.caption(f"📊 Word count: {len(content.split())} words")

    # Main action button
    st.markdown('<div class="analyze-button">', unsafe_allow_html=True)
    if st.button("⚡ Analyze & Improve How-to Guide", type="primary"):
            # Clear previous results
            for key in ["analysis_report", "final_document", "success", "original_word_count"]:
                st.session_state.pop(key, None)
            
            st.session_state["original_word_count"] = len(content.split())
            
            # Create document metadata
            doc_metadata = {
                'title': 'How-to Guide',
                'type': 'How-to Guide', 
                'category': 'General',
                'template': 'The Good Docs Project How-to Template',
                'length': st.session_state["original_word_count"]
            }
            
            # Processing phases
            with st.spinner("🤖 AI agents are analyzing your document..."):
                try:
                    # Phase 1: Document Analysis
                    st.info("📊 **Phase 1:** Analyzing document structure and content...")
                    
                    loop = asyncio.new_event_loop()
                    analysis_result = loop.run_until_complete(runner.run(document_analyzer, content))
                    loop.close()
                    st.session_state["analysis_report"] = analysis_result.final_output
                    
                    st.success("✅ Document analysis completed!")

                    # Phase 2: Style Enforcement
                    st.info("✨ **Phase 2:** Applying style improvements...")
                    
                    handoff_prompt = f"""
                    <document_metadata>
                    Title: {doc_metadata['title']}
                    Type: {doc_metadata['type']}
                    Word Count: {doc_metadata['length']}
                    </document_metadata>

                    <original_content>
                    {content}
                    </original_content>

                    <analysis_report>
                    {st.session_state["analysis_report"]}
                    </analysis_report>
                    
                    Please note: The final document should be a professional how-to guide and must not include any sections related to the "Content Assessment" or "Template Compliance," as this information is already present in the analysis report. Focus solely on producing the polished how-to guide content.
                    """
                    
                    loop = asyncio.new_event_loop()
                    enforced_result = loop.run_until_complete(runner.run(style_enforcer, handoff_prompt))
                    loop.close()
                    
                    # --- FIX: Extract content from XML tags ---
                    try:
                        root = ET.fromstring(enforced_result.final_output)
                        st.session_state["final_document"] = root.text.strip()
                    except ET.ParseError:
                        st.session_state["final_document"] = enforced_result.final_output

                    st.session_state["success"] = True
                    
                    st.success("✅ Style enforcement completed!")
                    st.balloons()

                except Exception as e:
                    st.session_state["success"] = False
                    st.error(f"❌ An error occurred during processing: {str(e)}")
                    st.info("💡 Please check your API key and try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Results Section ---
if st.session_state.get("final_document"):
    st.divider()
    st.markdown("## 📋 Analysis Results")
    
    # Create tabs for organized results
    tab1, tab2 = st.tabs(["📊 Analysis Report", "📝 Preview the draft "])
    
    with tab1:
        
        # Analysis report in an expandable text area
        st.text_area(
            "Analysis Report",
            value=st.session_state["analysis_report"],
            height=300,
            disabled=True,
            help="This report shows the AI's analysis of your how-to guide structure, step clarity, and template compliance"
        )
        
        # Key insights
        st.markdown("#### 💡 Quick Insights")
        analysis_text = st.session_state["analysis_report"].lower()
        if "missing" in analysis_text or "unclear" in analysis_text:
            st.warning("⚠️ Guide has unclear steps or missing template sections")
        if "improvement" in analysis_text or "better" in analysis_text:
            st.info("💡 AI found opportunities to improve step clarity and structure")
        if "good" in analysis_text or "clear" in analysis_text:
            st.success("✅ Guide shows good task-oriented structure")
            
        st.divider()
        
        # Guide Statistics and Writing Tips
        st.markdown("### 📈 Guide Statistics")
        original_words = st.session_state["original_word_count"]
        improved_words = len(st.session_state["final_document"].split())
        st.info(f"""
        **Statistics:**
        📝 Original: {original_words} words
        ✨ Improved: {improved_words} words
        📊 Change: {improved_words - original_words:+d} words
        """)
        
        st.markdown("### 💡 Professional Writing Tips")
        st.info("""
        **Tips:**
        • Use active voice over passive
        • Write in present tense
        • Keep sentences under 26 words
        • Be specific with UI elements
        • Remove filler words
        • Use consistent terminology
        """)

    with tab2:
        st.markdown("### 📝 Your Draft How-to Guide")
        
        # Improved document display
        st.text_area(
            "Final How-to Guide",
            value=st.session_state["final_document"],
            height=400,
            help="Your how-to guide now follows The Good Docs Project template with clear steps, prerequisites, and troubleshooting"
        )
        
        # Download options
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="⬇️ Download How-to Guide",
                data=st.session_state["final_document"],
                file_name="how_to_guide.md",
                mime="text/markdown",
                help="Download your professional how-to guide as a Markdown file"
            )
        
        with col2:
            # Alternative format download
            st.download_button(
                label="📄 Download as TXT",
                data=st.session_state["final_document"],
                file_name="how_to_guide.txt",
                mime="text/plain",
                help="Download your how-to guide as a plain text file"
            )

    # Action buttons
    st.divider()
    if st.button("🔄 Analyze Another Document", use_container_width=True):
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key in ["analysis_report", "final_document", "success", "original_word_count"]:
                del st.session_state[key]
        st.rerun()


# --- Footer Information ---
st.divider()

# Footer
st.markdown("""
<div style='text-align: center; color: #6b7280; margin-top: 2rem; padding: 1rem; border-top: 1px solid #e5e7eb;'>
    <p>🤖 Powered by OpenAI • Built with Streamlit • Using The Good Docs Project Template Standards</p>
</div>
""", unsafe_allow_html=True)
