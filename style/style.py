# Enhanced styling for DocuAlign with improved navigation branding
CUSTOM_CSS = """
<style>
/* Import Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ========================================
   CSS Variables for Light/Dark Mode
   ======================================== */
:root {
    /* Light Mode */
    --bg-primary: #fafafa;
    --bg-secondary: #ffffff;
    --bg-tertiary: #f5f5f5;
    --text-primary: #1f2937;
    --text-secondary: #4b5563;
    --text-tertiary: #6b7280;
    --border: #e5e7eb;
    --accent: #2563eb;
    --accent-hover: #1d4ed8;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --info: #3b82f6;
    
    /* Track Changes Colors */
    --redline-insert-bg: #dcfce7;
    --redline-insert-text: #166534;
    --redline-delete-bg: #fee2e2;
    --redline-delete-text: #991b1b;
    --redline-modify-bg: #fef3c7;
    --redline-modify-text: #92400e;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-tertiary: #94a3b8;
        --border: #475569;
        --accent: #60a5fa;
        --accent-hover: #3b82f6;
        --success: #34d399;
        --warning: #fbbf24;
        --error: #f87171;
        --info: #60a5fa;
        
        /* Track Changes Colors - Dark Mode */
        --redline-insert-bg: rgba(16, 185, 129, 0.2);
        --redline-insert-text: #6ee7b7;
        --redline-delete-bg: rgba(248, 113, 113, 0.2);
        --redline-delete-text: #fca5a5;
        --redline-modify-bg: rgba(251, 191, 36, 0.2);
        --redline-modify-text: #fcd34d;
    }
}

/* ========================================
   Global Styles
   ======================================== */
.stApp {
    background-color: var(--bg-primary);
    font-family: "Inter", sans-serif;
    color: var(--text-primary);
}

* {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ========================================
   Navigation Header (Enhanced with Branding)
   ======================================== */
.nav-header-static {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-bottom: none;
    padding: 1.25rem 0;
    margin-bottom: 2rem;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.nav-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 2rem;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.nav-icon {
    font-size: 2rem;
    background: white;
    padding: 0.5rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    width: 3.5rem;
    height: 3.5rem;
    transition: transform 0.2s;
}

.nav-icon:hover {
    transform: scale(1.05);
}

.nav-text {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.nav-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: white;
    letter-spacing: -0.02em;
    line-height: 1;
}

.nav-subtitle {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.85);
    font-weight: 500;
    letter-spacing: 0.01em;
}

/* Hide default Streamlit header */
header[data-testid="stHeader"] {
    display: none;
}

/* ========================================
   Main Container (Simplified)
   ======================================== */
.main .block-container {
    max-width: 900px;
    padding: 2rem 2.5rem;
    margin: 0 auto;
}

/* ========================================
   Typography
   ======================================== */
.headline {
    text-align: center;
    font-size: 2.25rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
    margin-bottom: 1rem;
}

.headline .highlight {
    color: var(--accent);
}

.subtext {
    text-align: center;
    color: var(--text-secondary);
    font-size: 1.125rem;
    line-height: 1.6;
    max-width: 700px;
    margin: 0 auto 2.5rem;
}

h2 {
    color: var(--text-primary);
    font-weight: 600;
    font-size: 1.5rem;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
}

h3 {
    color: var(--text-primary);
    font-weight: 600;
    font-size: 1.25rem;
    margin: 1.5rem 0 1rem 0;
}

/* ========================================
   Forms & Inputs (Simplified)
   ======================================== */
.stTextInput input,
.stTextArea textarea {
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem;
    font-size: 1rem;
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    transition: border-color 0.2s;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--accent);
    outline: none;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

@media (prefers-color-scheme: dark) {
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
    }
}

/* Fix disabled textarea visibility */
textarea:disabled {
    background-color: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    opacity: 1 !important;
}

/* Labels */
.stTextInput label,
.stTextArea label,
.stFileUploader label {
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 0.95rem;
}

/* ========================================
   File Uploader (Simplified)
   ======================================== */
.stFileUploader {
    border: 2px dashed var(--border);
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    background: var(--bg-secondary);
    transition: border-color 0.3s;
}

.stFileUploader:hover {
    border-color: var(--accent);
    background-color: var(--bg-tertiary);
}

/* ========================================
   Buttons (Simplified & Modern)
   ======================================== */
.stButton > button,
button[data-testid="baseButton-primary"] {
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.2s;
    cursor: pointer;
}

.stButton > button:hover,
button[data-testid="baseButton-primary"]:hover {
    background: var(--accent-hover);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

@media (prefers-color-scheme: dark) {
    .stButton > button:hover,
    button[data-testid="baseButton-primary"]:hover {
        box-shadow: 0 4px 12px rgba(96, 165, 250, 0.4);
    }
}

/* Main analyze button */
.analyze-button button {
    width: 100%;
    height: 3rem;
    font-size: 1.1rem;
    margin: 1rem 0;
}

/* Download buttons */
button[kind="secondary"] {
    background: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
}

button[kind="secondary"]:hover {
    background: var(--bg-secondary) !important;
    border-color: var(--accent) !important;
}

/* ========================================
   Tabs (Enhanced for 4-tab layout)
   ======================================== */
.stTabs {
    margin-top: 1.5rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background-color: var(--bg-tertiary);
    padding: 0.5rem;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: var(--text-tertiary);
    border-radius: 6px;
    font-weight: 500;
    padding: 0.75rem 1.25rem;
    transition: all 0.2s;
}

.stTabs [aria-selected="true"] {
    background-color: var(--bg-secondary);
    color: var(--accent);
    font-weight: 600;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

@media (prefers-color-scheme: dark) {
    .stTabs [aria-selected="true"] {
        color: var(--accent);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
}

/* ========================================
   Track Changes Styling
   ======================================== */

/* Redline markup elements */
.redline-insert,
mark[data-type="insert"],
strong:has(+ em[contains(text(), "INSERT")]) {
    background-color: var(--redline-insert-bg);
    color: var(--redline-insert-text);
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 600;
    border: 1px solid var(--redline-insert-text);
}

.redline-delete,
del,
s {
    background-color: var(--redline-delete-bg);
    color: var(--redline-delete-text);
    padding: 2px 6px;
    border-radius: 4px;
    text-decoration: line-through;
    border: 1px solid var(--redline-delete-text);
}

.redline-modify {
    background-color: var(--redline-modify-bg);
    color: var(--redline-modify-text);
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 500;
    border: 1px solid var(--redline-modify-text);
}

/* Track changes legend */
.track-changes-legend {
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
}

/* ========================================
   Markdown Content (Enhanced Readability)
   ======================================== */
.stMarkdown {
    color: var(--text-primary);
    line-height: 1.6;
}

.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3 {
    color: var(--text-primary);
}

.stMarkdown p,
.stMarkdown li,
.stMarkdown span {
    color: var(--text-primary);
}

.stMarkdown code {
    background-color: var(--bg-tertiary);
    color: var(--accent);
    padding: 0.2em 0.4em;
    border-radius: 4px;
    font-size: 0.875em;
    border: 1px solid var(--border);
}

.stMarkdown pre {
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1rem;
    overflow-x: auto;
}

.stMarkdown pre code {
    background: none;
    border: none;
    padding: 0;
}

/* ========================================
   Alerts & Notifications (Simplified)
   ======================================== */
.stAlert,
div[data-testid="stNotification"] {
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    border-left: 4px solid;
}

.stSuccess {
    background-color: rgba(16, 185, 129, 0.1);
    border-left-color: var(--success);
    color: var(--text-primary);
}

.stInfo {
    background-color: rgba(59, 130, 246, 0.1);
    border-left-color: var(--info);
    color: var(--text-primary);
}

.stWarning {
    background-color: rgba(245, 158, 11, 0.1);
    border-left-color: var(--warning);
    color: var(--text-primary);
}

.stError {
    background-color: rgba(239, 68, 68, 0.1);
    border-left-color: var(--error);
    color: var(--text-primary);
}

/* ========================================
   Metrics (Simplified)
   ======================================== */
div[data-testid="metric-container"] {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
}

div[data-testid="metric-container"] label {
    color: var(--text-tertiary);
    font-size: 0.875rem;
    font-weight: 500;
}

div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: var(--text-primary);
    font-size: 1.875rem;
    font-weight: 700;
}

/* ========================================
   Expanders (Simplified)
   ======================================== */
.streamlit-expanderHeader {
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-primary);
    font-weight: 500;
    padding: 0.75rem 1rem;
}

.streamlit-expanderHeader:hover {
    background-color: var(--bg-secondary);
}

.streamlit-expanderContent {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 1rem;
}

/* ========================================
   Sidebar (Simplified)
   ======================================== */
.sidebar .block-container {
    background-color: var(--bg-secondary);
    border-radius: 8px;
    padding: 1.5rem;
    border: 1px solid var(--border);
}

.sidebar .stMarkdown h3 {
    color: var(--text-primary);
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

/* ========================================
   Tables (Enhanced)
   ======================================== */
.stDataFrame,
table {
    width: 100%;
    border-collapse: collapse;
    background-color: var(--bg-secondary);
}

.stDataFrame th,
table th {
    background-color: var(--bg-tertiary);
    color: var(--text-primary);
    font-weight: 600;
    padding: 0.75rem;
    text-align: left;
    border: 1px solid var(--border);
}

.stDataFrame td,
table td {
    padding: 0.75rem;
    border: 1px solid var(--border);
    color: var(--text-primary);
}

.stDataFrame tr:hover,
table tr:hover {
    background-color: var(--bg-tertiary);
}

/* ========================================
   Divider
   ======================================== */
hr {
    border: none;
    height: 1px;
    background-color: var(--border);
    margin: 2rem 0;
}

/* ========================================
   Responsive Design
   ======================================== */
@media (max-width: 768px) {
    .nav-container,
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    .nav-icon {
        width: 3rem;
        height: 3rem;
        font-size: 1.5rem;
    }
    
    .nav-title {
        font-size: 1.5rem;
    }
    
    .nav-subtitle {
        font-size: 0.75rem;
    }
    
    .headline {
        font-size: 1.75rem;
    }
    
    .subtext {
        font-size: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 0.75rem;
        font-size: 0.875rem;
    }
}

/* ========================================
   Focus States (Accessibility)
   ======================================== */
button:focus,
input:focus,
textarea:focus,
select:focus {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}

/* ========================================
   Spinner/Loading
   ======================================== */
.stSpinner > div {
    border-color: var(--accent);
    border-right-color: transparent;
}

/* ========================================
   Dark Mode Text Fixes
   ======================================== */
@media (prefers-color-scheme: dark) {
    /* Ensure all text is visible */
    .stMarkdown *,
    .streamlit-expanderContent *,
    div[data-testid="stText"],
    p, span, div, li {
        color: var(--text-primary) !important;
    }
    
    /* Links */
    a {
        color: var(--accent) !important;
        text-decoration: underline;
    }
    
    a:hover {
        color: var(--accent-hover) !important;
    }
    
    /* Code blocks */
    .stMarkdown code {
        background-color: var(--bg-tertiary) !important;
        color: var(--accent) !important;
    }
    
    /* Lists */
    .stMarkdown ul li::marker,
    .stMarkdown ol li::marker {
        color: var(--accent) !important;
    }
}

/* ========================================
   Special: Side-by-Side Comparison
   ======================================== */
.comparison-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 1rem 0;
}

@media (max-width: 768px) {
    .comparison-container {
        grid-template-columns: 1fr;
    }
}

/* ========================================
   Special: Quality Status Badges
   ======================================== */
.status-pass {
    color: var(--success);
    font-weight: 600;
}

.status-fail {
    color: var(--error);
    font-weight: 600;
}

/* ========================================
   Simplified Animation
   ======================================== */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.main .block-container {
    animation: fadeIn 0.4s ease-out;
}

</style>
"""