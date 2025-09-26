import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
from xml.etree import ElementTree as ET
from datetime import datetime
import json

# Load environment variables from the .env file
load_dotenv()

# Import the custom CSS from the new style folder
from style.style import CUSTOM_CSS

# Import the agents and runner
from components.agents import Agent, Runner
from components.analyzer import document_analyzer
from components.enforcer import style_enforcer

# Import evaluation components
from components.evaluation.evaluator import DocumentEvaluator
from components.evaluation.dashboard import render_evaluation_section

# --- Page Configuration and CSS ---
st.set_page_config(
    page_title="Docu-Align — AI-powered Documentation",
    page_icon="📝"
    # Removed layout="centered" to show default Streamlit header
)

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state["page"] = "main"

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
# Inject CSS to override default text area color and fix content preview color
st.markdown("""
<style>
/* Target the text within disabled text areas to make it black */
textarea:disabled {
    -webkit-text-fill-color: black;
    color: black;
    opacity: 1; /* Ensure full opacity */
}
/* New rule to ensure readability in the content preview section */
.st-expander div[data-testid="stText"] {
    color: #333 !important; /* Forces text to be a dark gray */
}
/* FORCE STREAMLIT HEADER AND DEPLOY BUTTON VISIBILITY */
header[data-testid="stHeader"] {
    display: block !important;
    visibility: visible !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 999999 !important;
    background: white !important;
    height: auto !important;
}
/* Ensure deploy button container is visible */
div[data-testid="stToolbar"] {
    display: flex !important;
    visibility: visible !important;
    z-index: 999999 !important;
}
/* Force deploy button visibility */
button[title*="Deploy"], button[aria-label*="Deploy"] {
    display: block !important;
    visibility: visible !important;
    z-index: 999999 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Navigation Header (Updated to non-fixed) ---
st.markdown("""
<div class="nav-header-static">
    <div class="nav-container">
        <div class="nav-brand">
            <span class="nav-title">DocuAlign</span>
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

# --- Sidebar Navigation ---
st.sidebar.markdown("### 📊 Quality & Evaluation")

if st.sidebar.button("📊 View Quality Dashboard", use_container_width=True):
    st.session_state["page"] = "evaluations"

if st.sidebar.button("🔄 Return to Main App", use_container_width=True):
    st.session_state["page"] = "main"

st.sidebar.markdown("---")

# Show evaluation summary in sidebar if data exists
try:
    evaluator = DocumentEvaluator()
    summary = evaluator.get_evaluation_summary()
    if summary['total_evaluations'] > 0:
        st.sidebar.markdown("**🎯 Recent Quality Stats**")
        st.sidebar.metric("Documents Processed", summary['total_evaluations'])
        st.sidebar.metric("Overall Pass Rate", f"{summary['overall_pass_rate']:.1f}%")
        st.sidebar.metric("Technical Accuracy", f"{summary['h7_pass_rate']:.1f}%")
except Exception as e:
    pass  # Silently handle any evaluation loading errors

# --- Page Routing ---
if st.session_state.get("page") == "evaluations":
    render_evaluation_section()
    st.stop()  # Don't render the rest of the main app

# --- Main Application Layout ---

# Modern headline with highlighted text
st.markdown(
    '<div class="headline">Transform your <span class="highlight">how-to guides</span> with our AI-powered documentation system</div>',
    unsafe_allow_html=True
)

# Descriptive subtext
st.markdown(
    '<div class="subtext">Upload your draft how-to content and watch as our AI improves it into a structured, how-to guide following The Good Docs Project template standards.</div>',
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
        for key in ["analysis_report", "final_document", "success", "original_word_count", "evaluation_results"]:
            st.session_state.pop(key, None)
        
        st.session_state["original_word_count"] = len(content.split())
        
        # Initialize evaluator
        evaluator = DocumentEvaluator()
        
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

                st.success("✅ Style enforcement completed!")
                
                # Phase 3: Quality Evaluation (NEW!)
                st.info("📊 **Phase 3:** Running quality evaluation...")
                
                loop = asyncio.new_event_loop()
                evaluation_results = loop.run_until_complete(
                    evaluator.evaluate_output(
                        original_content=content,
                        analysis_report=st.session_state["analysis_report"],
                        final_output=st.session_state["final_document"],
                        user_id=st.session_state.get("user_id", "anonymous")
                    )
                )
                loop.close()
                
                st.session_state["evaluation_results"] = evaluation_results
                st.session_state["success"] = True
                
                st.success("✅ Quality evaluation completed!")
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
            st.warning("⚠️ The doc has unclear steps or missing template sections")
        if "improvement" in analysis_text or "better" in analysis_text:
            st.info("💡 We found opportunities to improve step clarity and structure")
        if "good" in analysis_text or "clear" in analysis_text:
            st.success("✅ The doc shows good task-oriented structure")
            
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
        
        st.markdown("### 💡 Tech 101 writing tips")
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
        st.markdown("### 📝 Your draft is ready")
        
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
                label="⬇️ Download as Markdown",
                data=st.session_state["final_document"],
                file_name="Draft",
                mime="text/markdown",
                help="Download as Markdown"
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

    # --- Quality Assessment Section (NEW!) ---
    if st.session_state.get("evaluation_results"):
        st.divider()
        st.markdown("## 📊 Quality Assessment")
        
        evaluation_results = st.session_state["evaluation_results"]
        
        # Overall quality indicator
        critical_pass = evaluation_results['h7_pass'] and evaluation_results['h8_pass'] and evaluation_results['h9_pass']
        
        if critical_pass:
            st.success("🎉 **High Quality Output** - All critical evaluation criteria passed!")
        else:
            st.warning("⚠️ **Review Recommended** - Some quality criteria need attention.")
        
        # Quality metrics in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            h7_status = "✅ PASS" if evaluation_results['h7_pass'] else "❌ FAIL"
            st.metric(
                "Technical Accuracy (H7)", 
                h7_status, 
                f"Score: {evaluation_results['h7_accuracy_score']}/5"
            )
            if not evaluation_results['h7_pass']:
                st.caption("⚠️ CRITICAL: Technical elements may have been altered")
        
        with col2:
            h8_status = "✅ PASS" if evaluation_results['h8_pass'] else "❌ FAIL"
            st.metric(
                "Style Compliance (H8)", 
                h8_status, 
                f"Score: {evaluation_results['h8_style_score']}/5"
            )
            if not evaluation_results['h8_pass']:
                st.caption("⚠️ CRITICAL: Style guide rules not followed")
        
        with col3:
            h9_status = "✅ PASS" if evaluation_results['h9_pass'] else "❌ FAIL"
            st.metric(
                "Gap Resolution (H9)", 
                h9_status, 
                f"Score: {evaluation_results['h9_gap_resolution_score']}/5"
            )
            if not evaluation_results['h9_pass']:
                st.caption("⚠️ CRITICAL: Identified issues not properly resolved")
        
        # Detailed evaluation results
        with st.expander("🔍 Detailed Quality Analysis", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Quality Metrics**")
                st.write(f"• Overall Quality Score: {evaluation_results['overall_score']:.1f}/5.0")
                st.write(f"• Word Count Change: {evaluation_results['final_word_count'] - evaluation_results['original_word_count']:+d} words")
            
            with col2:
                st.markdown("**🔍 Issue Summary**")
                st.write(f"• Technical Issues: {evaluation_results.get('h7_issues', 'None detected')}")
                st.write(f"• Style Violations: {evaluation_results.get('h8_violations', 'None detected')}")
                st.write(f"• Gap Resolution: {evaluation_results.get('h9_gaps_fixed', 'Completed')}")
        
        # User feedback collection
        with st.expander("💬 Provide Feedback (Optional)", expanded=False):
            st.markdown("Help us improve DocuAlign by rating this output:")
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                user_rating = st.select_slider(
                    "How would you rate the overall output quality?",
                    options=[1, 2, 3, 4, 5],
                    value=4,
                    help="1=Poor, 2=Below Average, 3=Average, 4=Good, 5=Excellent"
                )
            
            with col2:
                user_feedback = st.text_area(
                    "Additional comments (optional):",
                    placeholder="What worked well? What could be improved?",
                    height=80
                )
            
            if st.button("📝 Submit Feedback"):
                # Here you could save the feedback to your evaluation system
                st.success("🙏 Thank you for your feedback! This helps us improve DocuAlign.")
                
        # Quick access to evaluation dashboard
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 View Quality Dashboard", use_container_width=True):
                st.session_state["page"] = "evaluations"
                st.rerun()
        
        with col2:
            if st.button("📥 Export Evaluation Data", use_container_width=True):
                # Create a simple evaluation export
                eval_data = {
                    'document_evaluation': evaluation_results,
                    'timestamp': datetime.now().isoformat(),
                    'quality_summary': {
                        'technical_accuracy': evaluation_results['h7_pass'],
                        'style_compliance': evaluation_results['h8_pass'],
                        'gap_resolution': evaluation_results['h9_pass'],
                        'overall_quality': evaluation_results['overall_pass']
                    }
                }
                
                st.download_button(
                    label="Download Evaluation JSON",
                    data=json.dumps(eval_data, indent=2),
                    file_name=f"docualign_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

    # Action buttons
    st.divider()
    if st.button("🔄 Analyze Another Document", use_container_width=True):
        # Clear all session state
        for key in list(st.session_state.keys()):
            if key in ["analysis_report", "final_document", "success", "original_word_count", "evaluation_results"]:
                del st.session_state[key]
        st.rerun()


# --- Footer Information ---
st.divider()

# Footer
st.markdown("""
<div style='text-align: center; color: #6b7280; margin-top: 2rem; padding: 1rem; border-top: 1px solid #e5e7eb;'>
    <p>🤖 Powered by OpenAI • Built with Streamlit • Using The Good Docs Project Template Standards</p>
    <p style='font-size: 0.8rem; margin-top: 0.5rem;'>📊 Quality evaluation powered by HHH Framework (Helpful, Honest, Harmless)</p>
</div>
""", unsafe_allow_html=True)