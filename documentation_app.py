"""
Enhanced Documentation App with Track Changes Support
- Two-agent pipeline: Document Analyzer → Style Enforcer
- Safe evaluation handling with fallback for missing keys
- 4-tab results: Structure Analysis, Track Changes, Final Draft, Quality Report
- Good Docs Project validation with soft rejection
- UI IMPROVEMENTS: Progress stepper, metric cards, toast notifications, improved empty state
"""

import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
from xml.etree import ElementTree as ET
from datetime import datetime
import json
import re

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

# --- Helper Functions ---
def render_metric_card(title: str, value: str, status: str, icon: str, score: str = ""):
    """Render a modern metric card"""
    status_colors = {
        "pass": {"bg": "#dcfce7", "border": "#10b981", "text": "#166534"},
        "fail": {"bg": "#fee2e2", "border": "#ef4444", "text": "#991b1b"},
        "warning": {"bg": "#fef3c7", "border": "#f59e0b", "text": "#92400e"}
    }
    
    colors = status_colors.get(status, status_colors["warning"])
    score_html = f"<div style='font-size: 14px; color: {colors['text']}; opacity: 0.8; margin-top: 4px;'>{score}</div>" if score else ""
    
    st.markdown(f"""
    <div style='background: {colors["bg"]}; 
                border-left: 4px solid {colors["border"]}; 
                border-radius: 8px; padding: 1.5rem; margin: 0.5rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <div style='font-size: 36px;'>{icon}</div>
            <div style='flex: 1;'>
                <div style='font-size: 14px; color: {colors["text"]}; 
                           opacity: 0.8; font-weight: 500;'>{title}</div>
                <div style='font-size: 24px; color: {colors["text"]}; 
                           font-weight: 700; margin-top: 4px;'>{value}</div>
                {score_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_word_count_comparison():
    """Render word count comparison visual"""
    if st.session_state.get("original_word_count"):
        original_wc = st.session_state["original_word_count"]
        final_wc = len(st.session_state["final_document"].split())
        change = final_wc - original_wc
        change_pct = (change / original_wc) * 100 if original_wc > 0 else 0
        
        st.markdown(f"""
        <div style='display: flex; gap: 1rem; align-items: center; 
                    padding: 1rem; background: #f3f4f6; border-radius: 8px; margin: 1rem 0;'>
            <div style='flex: 1; text-align: center;'>
                <div style='font-size: 12px; color: #6b7280;'>Original</div>
                <div style='font-size: 24px; font-weight: 700;'>{original_wc}</div>
                <div style='font-size: 12px;'>words</div>
            </div>
            <div style='font-size: 32px; color: #2563eb;'>→</div>
            <div style='flex: 1; text-align: center;'>
                <div style='font-size: 12px; color: #6b7280;'>Final</div>
                <div style='font-size: 24px; font-weight: 700; color: {"#10b981" if change >= 0 else "#ef4444"};'>{final_wc}</div>
                <div style='font-size: 12px;'>words ({change:+d}, {change_pct:+.1f}%)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def parse_analyzer_output(output: str) -> dict:
    """
    Parse the three sections from Document Analyzer output:
    - Structure Analysis
    - Redlined Version
    - Clean Draft
    """
    sections = {
        'structure_analysis': '',
        'redlined_version': '',
        'clean_draft': ''
    }
    
    # Extract Structure Analysis section
    analysis_match = re.search(
        r'## 📊 Structure Analysis.*?(?=## 🔴 REDLINED VERSION|$)', 
        output, 
        re.DOTALL
    )
    if analysis_match:
        sections['structure_analysis'] = analysis_match.group(0).strip()
    
    # Extract Redlined Version section
    redline_match = re.search(
        r'## 🔴 REDLINED VERSION.*?(?=## ✨ CLEAN DRAFT|$)', 
        output, 
        re.DOTALL
    )
    if redline_match:
        sections['redlined_version'] = redline_match.group(0).strip()
    
    # Extract Clean Draft section
    draft_match = re.search(
        r'## ✨ CLEAN DRAFT.*?(?=$)', 
        output, 
        re.DOTALL
    )
    if draft_match:
        # Remove the header and handoff note
        draft_text = draft_match.group(0).strip()
        # Remove "HANDOFF NOTE FOR STYLE ENFORCER" section
        draft_text = re.sub(r'\*\*HANDOFF NOTE.*?---', '', draft_text, flags=re.DOTALL)
        sections['clean_draft'] = draft_text.strip()
    
    return sections


def extract_clean_content(text: str) -> str:
    """Remove XML tags if present"""
    try:
        root = ET.fromstring(text)
        return root.text.strip()
    except ET.ParseError:
        return text


# --- Page Configuration and CSS ---
st.set_page_config(
    page_title="DocuAlign — AI-powered Documentation",
    page_icon="📝"
)

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state["page"] = "main"

# Inject custom CSS with pulse animation
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Enhanced Navigation CSS (ensure it loads)
st.markdown("""
<style>
/* Enhanced Navigation Header */
.nav-header-static {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-bottom: none !important;
    padding: 1.25rem 0 !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1) !important;
}

.nav-brand {
    display: flex !important;
    align-items: center !important;
    gap: 1rem !important;
}

.nav-icon {
    font-size: 2rem !important;
    background: white !important;
    padding: 0.5rem !important;
    border-radius: 12px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    width: 3.5rem !important;
    height: 3.5rem !important;
}

.nav-text {
    display: flex !important;
    flex-direction: column !important;
    gap: 0.25rem !important;
}

.nav-title {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: white !important;
    letter-spacing: -0.02em !important;
    line-height: 1 !important;
}

.nav-subtitle {
    font-size: 0.875rem !important;
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Target the text within disabled text areas to make it black */
textarea:disabled {
    -webkit-text-fill-color: black;
    color: black;
    opacity: 1;
}
/* New rule to ensure readability in the content preview section */
.st-expander div[data-testid="stText"] {
    color: #333 !important;
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
/* Redline styling for track changes */
.redline-insert {
    background-color: #d4edda;
    color: #155724;
    padding: 2px 4px;
    border-radius: 3px;
}
.redline-delete {
    background-color: #f8d7da;
    color: #721c24;
    text-decoration: line-through;
    padding: 2px 4px;
    border-radius: 3px;
}
.redline-modify {
    background-color: #fff3cd;
    color: #856404;
    padding: 2px 4px;
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)

# --- Navigation Header ---
st.markdown("""
<div class="nav-header-static">
    <div class="nav-container">
        <div class="nav-brand">
            <span class="nav-icon">📝</span>
            <div class="nav-text">
                <span class="nav-title">DocuAlign</span>
                <span class="nav-subtitle">AI-Powered Documentation</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Agent Initialization ---
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
    pass

# --- Page Routing ---
if st.session_state.get("page") == "evaluations":
    render_evaluation_section()
    st.stop()

# --- Main Application Layout ---

# Modern headline
st.markdown(
    '<div class="headline">Transform your <span class="highlight">drafts</span> with our AI-powered documentation system</div>',
    unsafe_allow_html=True
)

st.divider()

# --- Upload Section ---
st.markdown("## 📄 Upload Your Document")

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

# --- Empty State (when no content) ---
if not content:
    st.divider()
    st.markdown("""
    <div style='text-align: center; padding: 3rem 1rem; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 16px; color: white; margin: 2rem 0;'>
        <div style='font-size: 48px; margin-bottom: 1rem;'>📝</div>
        <h2 style='color: white; margin-bottom: 1rem;'>Ready to Transform Your Documentation</h2>
        <p style='font-size: 18px; opacity: 0.9; margin-bottom: 2rem;'>
            Upload a document or paste content above to get started
        </p>
        <div style='display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;'>
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; min-width: 150px;'>
                <div style='font-size: 32px;'>⚡</div>
                <div style='font-size: 14px; margin-top: 0.5rem;'>Fast Processing</div>
            </div>
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; min-width: 150px;'>
                <div style='font-size: 32px;'>✨</div>
                <div style='font-size: 14px; margin-top: 0.5rem;'>AI-Powered</div>
            </div>
            <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; min-width: 150px;'>
                <div style='font-size: 32px;'>📊</div>
                <div style='font-size: 14px; margin-top: 0.5rem;'>Quality Reports</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        for key in ["structure_analysis", "redlined_version", "clean_draft", "final_document", 
                    "success", "original_word_count", "evaluation_results", "type_mismatch"]:
            st.session_state.pop(key, None)
        
        st.session_state["original_word_count"] = len(content.split())
        st.session_state["original_content"] = content
        
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
        
        # CONSOLIDATED PROGRESS BLOCK
        progress_container = st.container()
        
        with progress_container:
            # Single progress placeholder
            progress_text = st.empty()
            status_text = st.empty()
            
            try:
                # Phase 1: Document Analysis with Type Validation
                progress_text.info("**Phase 1 of 3:** 📊 Validating document type and analyzing structure...")
                
                loop = asyncio.new_event_loop()
                analysis_result = loop.run_until_complete(runner.run(document_analyzer, content))
                loop.close()
                
                # ============================================
                # CHECK FOR SOFT REJECTION FIRST
                # ============================================
                if "⚠️ DOCUMENT TYPE MISMATCH" in analysis_result.final_output:
                    # Document failed validation - show soft rejection
                    st.session_state["type_mismatch"] = True
                    st.session_state["rejection_message"] = analysis_result.final_output
                    st.session_state["success"] = False
                    
                    # Display rejection message
                    st.error("### ⚠️ Document Type Validation Failed")
                    st.markdown(analysis_result.final_output)
                    
                    # Helpful guidance section
                    st.divider()
                    st.info("💡 **Quick Fix Guide**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("""
                        **✅ How-to Guide Must Have:**
                        - Numbered steps (1, 2, 3...)
                        - Action verbs (Click, Enter, Select)
                        - One specific task
                        - Prerequisites section
                        """)
                    
                    with col2:
                        st.markdown("""
                        **📝 Quick Template:**
                        ```
                        # [Task Title]
                        
                        ## Overview
                        [What this accomplishes]
                        
                        ## Before you start
                        - [Requirement 1]
                        - [Requirement 2]
                        
                        ## Steps
                        1. [Action verb] the [thing]
                        2. [Action verb] to [result]
                        3. [Verify] by [checking]
                        ```
                        """)
                    
                    st.stop()  # Stop processing here
                
                # ============================================
                # VALID HOW-TO - CONTINUE NORMAL PROCESSING
                # ============================================
                
                # Parse the three-part output
                parsed_output = parse_analyzer_output(analysis_result.final_output)
                
                st.session_state["structure_analysis"] = parsed_output['structure_analysis']
                st.session_state["redlined_version"] = parsed_output['redlined_version']
                st.session_state["clean_draft"] = parsed_output['clean_draft']
                
                status_text.success("✅ Phase 1 complete: Document validated!")

                # Phase 2: Style Enforcement
                progress_text.info("**Phase 2 of 3:** ✨ Applying Microsoft style guide...")
                
                loop = asyncio.new_event_loop()
                enforced_result = loop.run_until_complete(
                    runner.run(style_enforcer, st.session_state["clean_draft"])
                )
                loop.close()
                
                # Extract clean content from XML if present
                st.session_state["final_document"] = extract_clean_content(enforced_result.final_output)
                
                status_text.success("✅ Phase 2 complete: Style guide applied!")
                
                # Phase 3: Quality Evaluation
                progress_text.info("**Phase 3 of 3:** 📊 Running quality evaluation...")
                
                try:
                    loop = asyncio.new_event_loop()
                    evaluation_results = loop.run_until_complete(
                        evaluator.evaluate_output(
                            original_content=content,
                            analysis_report=st.session_state["structure_analysis"],
                            final_output=st.session_state["final_document"],
                            user_id=st.session_state.get("user_id", "anonymous")
                        )
                    )
                    loop.close()
                    
                    st.session_state["evaluation_results"] = evaluation_results
                    
                except Exception as eval_error:
                    # Create minimal evaluation results for display
                    st.session_state["evaluation_results"] = {
                        'evaluation_status': 'incomplete',
                        'error_message': str(eval_error),
                        'original_word_count': len(content.split()),
                        'final_word_count': len(st.session_state["final_document"].split())
                    }
                
                # Final success message
                progress_text.empty()
                status_text.success("🎉 **All phases complete!** Your how-to guide is ready.")
                st.session_state["success"] = True
                st.balloons()

            except Exception as e:
                progress_text.empty()
                status_text.empty()
                st.session_state["success"] = False
                st.error(f"❌ An error occurred during processing: {str(e)}")
                st.info("💡 Please check your input and try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Results Section ---
if st.session_state.get("final_document"):
    st.divider()
    st.markdown("## 📋 Analysis Results")
    
    # Word count comparison at the top
    render_word_count_comparison()
    
    # Create tabs for organized results
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Structure Analysis", 
        "🔴 Track Changes", 
        "📝 Final Draft",
        "📈 Quality Report"
    ])
    
    with tab1:
        st.markdown("### 📊 Good Docs Template Compliance")
        
        # Display the structure analysis
        structure_content = st.session_state["structure_analysis"]
        st.markdown(structure_content)
        
        # Check if table is missing and show warning
        if "| Section | Status | Assessment |" not in structure_content:
            st.warning("⚠️ **Compliance table not generated.** The analyzer may have encountered an issue. Please review the analysis above for key findings.")

    with tab2:
        st.markdown("### 🔴 Tracked Changes (Redline View)")
        st.markdown("""
        This view shows all changes made to your document:
        - **[INSERT: text]** - New content added
        - ~~Strikethrough~~ - Content removed
        - 🔄 Modified - Content changed
        """)
        
        st.markdown("---")
        
        # Display redlined version
        st.markdown(st.session_state["redlined_version"])
        
        # Download redlined version
        st.download_button(
            label="⬇️ Download Redlined Version",
            data=st.session_state["redlined_version"],
            file_name="redlined_document.md",
            mime="text/markdown",
            help="Download the tracked changes version for review"
        )

    with tab3:
        st.markdown("### 📝 Your Publication-Ready Draft")
        st.markdown("**Formatted according to:**")
        st.markdown("✅ Good Docs Project how-to template")
        st.markdown("✅ Microsoft Style Guide")
        
        # Improved document display
        st.text_area(
            "Final How-to Guide",
            value=st.session_state["final_document"],
            height=400,
            help="Your how-to guide now follows The Good Docs Project template with Microsoft style guide applied"
        )
        
        # Download options
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="⬇️ Download as Markdown",
                data=st.session_state["final_document"],
                file_name="howto_guide_final.md",
                mime="text/markdown",
                help="Download as Markdown"
            )
        
        with col2:
            st.download_button(
                label="📄 Download as TXT",
                data=st.session_state["final_document"],
                file_name="howto_guide_final.txt",
                mime="text/plain",
                help="Download as plain text file"
            )
        
        # Side-by-side comparison
        with st.expander("🔄 Compare Original vs Final", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original Document**")
                st.text_area(
                    "Original",
                    value=st.session_state["original_content"],
                    height=300,
                    disabled=True,
                    label_visibility="collapsed"
                )
            
            with col2:
                st.markdown("**Final Document**")
                st.text_area(
                    "Final",
                    value=st.session_state["final_document"],
                    height=300,
                    disabled=True,
                    label_visibility="collapsed"
                )

    with tab4:
        if st.session_state.get("evaluation_results"):
            st.markdown("### 📊 Quality Assessment Results")
            
            evaluation_results = st.session_state["evaluation_results"]
            
            # Safe key access with defaults
            h7_pass = evaluation_results.get('h7_pass', None)
            h8_pass = evaluation_results.get('h8_pass', None)
            h9_pass = evaluation_results.get('h9_pass', None)
            
            # Check if evaluation data is complete
            if h7_pass is None or h8_pass is None or h9_pass is None:
                st.warning("⚠️ **Evaluation data incomplete** - Some quality metrics are not available.")
                st.info("💡 This may happen if the evaluator encountered an error. The document was still processed successfully.")
                
                # Show available evaluation data
                with st.expander("🔍 Available Evaluation Data", expanded=True):
                    st.json(evaluation_results)
            else:
                # Overall quality indicator
                critical_pass = h7_pass and h8_pass and h9_pass
                
                if critical_pass:
                    st.success("🎉 **High Quality Output** - All critical evaluation criteria passed!")
                else:
                    st.warning("⚠️ **Review Recommended** - Some quality criteria need attention.")
                
                # Quality metrics using new card design
                h7_status = "pass" if h7_pass else "fail"
                h7_score = evaluation_results.get('h7_accuracy_score', 'N/A')
                h7_score_text = f"Score: {h7_score}/5" if h7_score != 'N/A' else "Score: N/A"
                render_metric_card("Technical Accuracy (H7)", "✅ PASS" if h7_pass else "❌ FAIL", h7_status, "🎯", h7_score_text)
                if not h7_pass:
                    st.caption("⚠️ CRITICAL: Technical elements may have been altered")
                
                h8_status = "pass" if h8_pass else "fail"
                h8_score = evaluation_results.get('h8_style_score', 'N/A')
                h8_score_text = f"Score: {h8_score}/5" if h8_score != 'N/A' else "Score: N/A"
                render_metric_card("Style Compliance (H8)", "✅ PASS" if h8_pass else "❌ FAIL", h8_status, "✨", h8_score_text)
                if not h8_pass:
                    st.caption("⚠️ CRITICAL: Style guide rules not followed")
                
                h9_status = "pass" if h9_pass else "fail"
                h9_score = evaluation_results.get('h9_gap_resolution_score', 'N/A')
                h9_score_text = f"Score: {h9_score}/5" if h9_score != 'N/A' else "Score: N/A"
                render_metric_card("Gap Resolution (H9)", "✅ PASS" if h9_pass else "❌ FAIL", h9_status, "🔍", h9_score_text)
                if not h9_pass:
                    st.caption("⚠️ CRITICAL: Identified issues not properly resolved")
                
                # Detailed evaluation results
                with st.expander("🔍 Detailed Quality Analysis", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**📊 Quality Metrics**")
                        overall_score = evaluation_results.get('overall_score', 'N/A')
                        st.write(f"• Overall Quality Score: {overall_score:.1f}/5.0" if overall_score != 'N/A' else "• Overall Quality Score: N/A")
                        
                        original_wc = evaluation_results.get('original_word_count', 0)
                        final_wc = evaluation_results.get('final_word_count', 0)
                        if original_wc > 0 and final_wc > 0:
                            st.write(f"• Word Count Change: {final_wc - original_wc:+d} words")
                    
                    with col2:
                        st.markdown("**🔍 Issue Summary**")
                        st.write(f"• Technical Issues: {evaluation_results.get('h7_issues', 'None detected')}")
                        st.write(f"• Style Violations: {evaluation_results.get('h8_violations', 'None detected')}")
                        st.write(f"• Gap Resolution: {evaluation_results.get('h9_gaps_fixed', 'Completed')}")
            
            # User feedback collection (always show)
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
                    st.success("🙏 Thank you for your feedback! This helps us improve DocuAlign.")
            
            # Export evaluation data (always show)
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 View Quality Dashboard", use_container_width=True):
                    st.session_state["page"] = "evaluations"
                    st.rerun()
            
            with col2:
                # Safe extraction for export
                eval_data = {
                    'document_evaluation': evaluation_results,
                    'timestamp': datetime.now().isoformat(),
                    'quality_summary': {
                        'technical_accuracy': evaluation_results.get('h7_pass', None),
                        'style_compliance': evaluation_results.get('h8_pass', None),
                        'gap_resolution': evaluation_results.get('h9_pass', None),
                        'overall_quality': evaluation_results.get('overall_pass', None)
                    }
                }
                
                st.download_button(
                    label="📥 Export Evaluation Data",
                    data=json.dumps(eval_data, indent=2),
                    file_name=f"docualign_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            # No evaluation results available
            st.info("📊 Quality evaluation will appear here after document processing.")

    # Action buttons
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Analyze Another Document", use_container_width=True):
            # Clear all session state
            for key in list(st.session_state.keys()):
                if key in ["structure_analysis", "redlined_version", "clean_draft", "final_document", 
                          "success", "original_word_count", "evaluation_results", "original_content"]:
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("📤 Share Results", use_container_width=True):
            st.info("💡 Download the files above and share them with your team!")


# --- Footer Information ---
st.divider()

st.markdown("""
<div style='text-align: center; color: #6b7280; margin-top: 2rem; padding: 1rem; border-top: 1px solid #e5e7eb;'>
    <p>🤖 Powered by OpenAI • Built with Streamlit • Using The Good Docs Project Template Standards</p>
    <p style='font-size: 0.8rem; margin-top: 0.5rem;'>📊 Quality evaluation powered by HHH Framework (Helpful, Honest, Harmless)</p>
    <p style='font-size: 0.8rem; margin-top: 0.5rem;'>✨ Style enforcement powered by Microsoft Style Guide</p>
</div>
""", unsafe_allow_html=True)