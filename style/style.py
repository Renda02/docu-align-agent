# Enhanced styling for Docu-Align App with Dark Mode Support
CUSTOM_CSS = """
<style>
/* Import Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* CSS Variables for Light/Dark Mode */
:root {
    --bg-primary: #fafafa;
    --bg-secondary: #ffffff;
    --bg-tertiary: #f9fafb;
    --text-primary: #1f2937;
    --text-secondary: #374151;
    --text-tertiary: #6b7280;
    --border-primary: #e5e7eb;
    --border-secondary: #d1d5db;
    --accent-primary: #1a9cff;
    --accent-secondary: #40bfff;
    --success: #22c55e;
    --warning: #f59e0b;
    --error: #ef4444;
    --shadow-light: rgba(0, 0, 0, 0.05);
    --shadow-medium: rgba(0, 0, 0, 0.1);
    --nav-bg: #ffffff;
    --input-bg: #ffffff;
    --card-bg: #ffffff;
}

/* Dark Mode Variables */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #e2e8f0;
        --text-tertiary: #cbd5e1;
        --border-primary: #475569;
        --border-secondary: #64748b;
        --accent-primary: #60a5fa;
        --accent-secondary: #3b82f6;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #f87171;
        --shadow-light: rgba(0, 0, 0, 0.3);
        --shadow-medium: rgba(0, 0, 0, 0.5);
        --nav-bg: #1e293b;
        --input-bg: #334155;
        --card-bg: #1e293b;
    }
}

/* Enhanced font rendering for better readability */
@media (prefers-color-scheme: dark) {
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
    }
}

/* Global styling */
.stApp {
    background-color: var(--bg-primary);
    font-family: "Inter", sans-serif;
    color: var(--text-primary);
}

/* Navigation header styling */
.nav-header {
    background-color: var(--nav-bg);
    border-bottom: 1px solid var(--border-primary);
    padding: 1rem 0;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 1000;
    box-shadow: 0 2px 4px var(--shadow-light);
    backdrop-filter: blur(10px);
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
}

.nav-logo {
    font-size: 1.2rem;
    background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary));
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.nav-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 2rem;
    padding-right: 10rem;
}

.nav-link {
    color: var(--text-tertiary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s ease;
    cursor: pointer;
}

.nav-link:hover {
    color: var(--accent-primary);
}



.nav-signin {
    background: linear-gradient(90deg, var(--accent-secondary), var(--accent-primary));
    color: white !important;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
    text-decoration: none;
}

.nav-signin:hover {
    background: linear-gradient(90deg, var(--accent-primary), #0d7de8);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(96, 165, 250, 0.3);
    color: white !important;
}

/* Hide Streamlit default header */
header[data-testid="stHeader"] {
    display: none;
}

/* Add this to ensure deploy button visibility */
div[data-testid="stToolbar"] {
    z-index: 1001 !important;
    margin-top: 60px !important;
}

/* Main container styling */
.main .block-container {
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    padding: 3rem 2.5rem;
    border-radius: 16px;
    margin: 80px auto 2rem auto;
    box-shadow: 0 4px 6px var(--shadow-light), 0 10px 15px var(--shadow-medium);
    max-width: 900px;
    border: 1px solid var(--border-primary);
}

/* Sidebar styling */
.sidebar .block-container {
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    border-radius: 12px;
    margin: 1rem;
    padding: 2rem 1.5rem;
    box-shadow: 0 2px 4px var(--shadow-light);
    border: 1px solid var(--border-primary);
}

/* Modern headline styling */
.headline {
    text-align: center;
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}

.headline .highlight {
    color: var(--accent-primary);
}

/* Subtext styling */
.subtext {
    text-align: center;
    color: var(--text-tertiary);
    font-size: 1.1rem;
    margin-bottom: 2.5rem;
    line-height: 1.6;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}

/* Typography */
h1 {
    text-align: center;
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}

h2 {
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 1.5rem;
    margin: 2rem 0 1rem 0;
    border-bottom: 2px solid var(--border-primary);
    padding-bottom: 0.5rem;
}

h3 {
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 1.25rem;
    margin: 1.5rem 0 1rem 0;
}

/* Input styling */
.stTextInput > div > div > input {
    border-radius: 10px;
    border: 1px solid var(--border-secondary);
    padding: 0.75rem 1rem;
    font-size: 1rem;
    color: var(--text-primary);
    background-color: var(--input-bg);
    transition: all 0.2s ease;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
    outline: none;
}

.stSelectbox > div > div > div {
    border-radius: 10px;
    border: 1px solid var(--border-secondary);
    padding: 0.5rem;
    background-color: var(--input-bg);
    color: var(--text-primary);
    transition: all 0.2s ease;
}

.stSelectbox > div > div > div:focus {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
}

/* Text area styling */
.stTextArea > div > div > textarea {
    border-radius: 10px;
    border: 1px solid var(--border-secondary);
    padding: 1rem;
    font-size: 1rem;
    color: var(--text-primary);
    background-color: var(--input-bg);
    line-height: 1.5;
    transition: all 0.2s ease;
}

.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
    outline: none;
}

/* Fix for disabled text areas in dark mode */
textarea:disabled {
    -webkit-text-fill-color: var(--text-primary) !important;
    color: var(--text-primary) !important;
    opacity: 0.8 !important;
    background-color: var(--bg-tertiary) !important;
}

/* Enhanced placeholder text visibility */
@media (prefers-color-scheme: dark) {
    input::placeholder,
    textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 0.8;
    }
    
    input:focus::placeholder,
    textarea:focus::placeholder {
        color: #cbd5e1 !important;
        opacity: 0.6;
    }
}

/* Improved text selection colors */
@media (prefers-color-scheme: dark) {
    ::selection {
        background-color: rgba(96, 165, 250, 0.3);
        color: #f1f5f9;
    }
    
    ::-moz-selection {
        background-color: rgba(96, 165, 250, 0.3);
        color: #f1f5f9;
    }
}

/* Labels */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stFileUploader label {
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}

/* Better form labels and help text */
@media (prefers-color-scheme: dark) {
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stFileUploader label,
    .stNumberInput label,
    .stDateInput label,
    .stTimeInput label {
        color: #cbd5e1 !important;
        font-weight: 500;
    }
    
    .help,
    .stHelp,
    [data-testid="stTooltipIcon"],
    .stTextInput + div,
    .stTextArea + div,
    .stSelectbox + div {
        color: #94a3b8 !important;
    }
}

/* File uploader styling */
.stFileUploader {
    border: 2px dashed var(--border-secondary);
    border-radius: 12px;
    padding: 2.5rem;
    text-align: center;
    background: var(--input-bg);
    margin: 1.5rem 0;
    transition: all 0.3s ease;
}

.stFileUploader:hover {
    border-color: var(--accent-primary);
    background-color: var(--bg-tertiary);
}

.stFileUploader label {
    color: var(--text-secondary);
    font-weight: 500;
}

/* Button styling */
.stButton > button {
    border-radius: 12px;
    background: linear-gradient(90deg, var(--accent-secondary), var(--accent-primary));
    color: white;
    font-weight: 600;
    height: 3.5rem;
    font-size: 1.1rem;
    border: none;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(96, 165, 250, 0.3);
    padding: 0 2rem;
    width: 100%;
    margin: 1rem 0;
}

.stButton > button:hover {
    background: linear-gradient(90deg, var(--accent-primary), #0d7de8);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(96, 165, 250, 0.4);
}

/* Primary button enhanced styling */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(90deg, var(--accent-secondary), var(--accent-primary)) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    height: 3.5rem !important;
    font-size: 1.1rem !important;
    box-shadow: 0 4px 12px rgba(96, 165, 250, 0.3) !important;
    width: 100% !important;
    margin: 1rem 0 !important;
    padding: 0 2rem !important;
}

button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(90deg, var(--accent-primary), #0d7de8) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(96, 165, 250, 0.4) !important;
}

/* Full width analyze button */
.analyze-button {
    width: 100%;
    margin: 2rem 0;
    text-align: center;
}

.analyze-button button {
    width: 100% !important;
    height: 3.5rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    background: linear-gradient(90deg, var(--accent-secondary), var(--accent-primary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(96, 165, 250, 0.3) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    display: block !important;
}

/* Secondary button styling */
.stButton > button[kind="secondary"] {
    background: var(--bg-secondary);
    color: var(--accent-primary);
    border: 2px solid var(--accent-primary);
    font-weight: 600;
}

.stButton > button[kind="secondary"]:hover {
    background: var(--bg-tertiary);
    border-color: var(--accent-primary);
    color: var(--accent-primary);
}

/* Alert styling with better contrast */
div[data-testid="stNotification"] {
    border-radius: 10px;
    border: none;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    font-weight: 500;
}

@media (prefers-color-scheme: dark) {
    div[data-testid="stNotification"][data-color="success"] {
        background-color: rgba(16, 185, 129, 0.1);
        color: #6ee7b7;
        border-left: 4px solid var(--success);
    }

    div[data-testid="stNotification"][data-color="info"] {
        background-color: rgba(96, 165, 250, 0.1);
        color: #93c5fd;
        border-left: 4px solid var(--accent-primary);
    }

    div[data-testid="stNotification"][data-color="warning"] {
        background-color: rgba(245, 158, 11, 0.1);
        color: #fbbf24;
        border-left: 4px solid var(--warning);
    }

    div[data-testid="stNotification"][data-color="error"] {
        background-color: rgba(248, 113, 113, 0.1);
        color: #fca5a5;
        border-left: 4px solid var(--error);
    }
}

@media (prefers-color-scheme: light) {
    div[data-testid="stNotification"][data-color="success"] {
        background-color: #f0fdf4;
        color: #166534;
        border-left: 4px solid var(--success);
    }

    div[data-testid="stNotification"][data-color="info"] {
        background-color: #eff6ff;
        color: #1e40af;
        border-left: 4px solid var(--accent-primary);
    }

    div[data-testid="stNotification"][data-color="warning"] {
        background-color: #fffbeb;
        color: #92400e;
        border-left: 4px solid var(--warning);
    }

    div[data-testid="stNotification"][data-color="error"] {
        background-color: #fef2f2;
        color: #dc2626;
        border-left: 4px solid var(--error);
    }
}

/* Better error and warning text visibility */
@media (prefers-color-scheme: dark) {
    .stAlert,
    .stError,
    .stWarning,
    .stInfo,
    .stSuccess {
        color: inherit !important;
    }
    
    .stError div,
    .stWarning div,
    .stInfo div,
    .stSuccess div {
        color: inherit !important;
    }
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border-primary);
    border-radius: 8px;
    color: var(--text-secondary);
    font-weight: 500;
    padding: 0.75rem 1rem;
    transition: all 0.2s ease;
}

.streamlit-expanderHeader:hover {
    background-color: var(--bg-tertiary);
    border-color: var(--border-secondary);
}

.streamlit-expanderContent {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-primary);
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 1rem;
    color: var(--text-primary);
}

/* Better expander text contrast */
@media (prefers-color-scheme: dark) {
    .streamlit-expanderHeader {
        color: #cbd5e1 !important;
        background-color: #334155 !important;
    }
    
    .streamlit-expanderContent {
        color: #e2e8f0 !important;
        background-color: #1e293b !important;
    }
    
    .streamlit-expanderContent .stMarkdown * {
        color: #e2e8f0 !important;
    }
}

/* Content preview fix */
.st-expander div[data-testid="stText"],
.st-expander .stMarkdown,
.streamlit-expanderContent * {
    color: var(--text-primary) !important;
}

/* Chat interface styling */
.stChatMessage {
    background-color: var(--card-bg);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 1rem 0;
    border: 1px solid var(--border-primary);
    box-shadow: 0 1px 3px var(--shadow-light);
    color: var(--text-primary);
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: var(--bg-tertiary);
    padding: 0.25rem;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: var(--text-tertiary);
    border-radius: 6px;
    font-weight: 500;
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background-color: var(--bg-secondary);
    color: var(--accent-primary);
    box-shadow: 0 1px 3px var(--shadow-light);
}

/* Enhanced tab text visibility */
@media (prefers-color-scheme: dark) {
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #60a5fa !important;
        font-weight: 600;
    }
}

/* Metric styling */
div[data-testid="metric-container"] {
    background-color: var(--card-bg);
    border: 1px solid var(--border-primary);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 1px 3px var(--shadow-light);
}

div[data-testid="metric-container"] label {
    color: var(--text-tertiary) !important;
    font-size: 0.875rem !important;
}

div[data-testid="metric-container"] div[data-testid="metric-value"] {
    color: var(--text-primary) !important;
    font-size: 1.875rem !important;
    font-weight: 600 !important;
}

/* Enhanced metric display readability */
@media (prefers-color-scheme: dark) {
    div[data-testid="metric-container"] {
        background-color: #1e293b !important;
        border-color: #475569 !important;
    }
    
    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
        font-size: 0.875rem !important;
        font-weight: 500;
    }
    
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Metric delta colors */
    div[data-testid="metric-container"] div[data-testid="metric-delta"] {
        color: #10b981 !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="metric-delta"].negative {
        color: #f87171 !important;
    }
}

/* Code block styling */
.stCode {
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border-primary);
    border-radius: 6px;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    color: var(--text-primary);
}

/* Enhanced code block readability */
@media (prefers-color-scheme: dark) {
    .stCode,
    code,
    pre {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
        text-shadow: none;
    }
    
    /* Inline code styling */
    .stMarkdown code:not(pre code) {
        background-color: rgba(51, 65, 85, 0.8) !important;
        color: #f1f5f9 !important;
        padding: 0.2em 0.4em !important;
        border-radius: 4px !important;
        font-size: 0.9em !important;
        border: 1px solid #475569;
    }
}

/* Markdown styling */
.stMarkdown {
    color: var(--text-primary);
    line-height: 1.6;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--text-primary) !important;
}

.stMarkdown p, .stMarkdown li, .stMarkdown span, .stMarkdown div {
    color: var(--text-primary) !important;
}

.stMarkdown blockquote {
    background-color: var(--bg-tertiary);
    border-left: 4px solid var(--border-secondary);
    padding: 0.5rem 1rem;
    margin: 1rem 0;
    border-radius: 0 4px 4px 0;
    color: var(--text-primary);
}

/* Better link colors and readability */
@media (prefers-color-scheme: dark) {
    a, 
    .stMarkdown a {
        color: #60a5fa !important;
        text-decoration: underline;
        text-decoration-color: rgba(96, 165, 250, 0.5);
        transition: all 0.2s ease;
    }
    
    a:hover,
    .stMarkdown a:hover {
        color: #93c5fd !important;
        text-decoration-color: #93c5fd;
        text-shadow: 0 0 8px rgba(96, 165, 250, 0.3);
    }
    
    a:visited,
    .stMarkdown a:visited {
        color: #a78bfa !important;
    }
}

/* Better blockquote styling */
@media (prefers-color-scheme: dark) {
    .stMarkdown blockquote {
        background-color: rgba(51, 65, 85, 0.5) !important;
        border-left: 4px solid #60a5fa !important;
        color: #cbd5e1 !important;
        font-style: italic;
    }
    
    .stMarkdown blockquote p {
        color: #cbd5e1 !important;
    }
}

/* Enhanced list styling in dark mode */
@media (prefers-color-scheme: dark) {
    .stMarkdown ul,
    .stMarkdown ol {
        color: #e2e8f0 !important;
    }
    
    .stMarkdown ul li,
    .stMarkdown ol li {
        color: #e2e8f0 !important;
        margin-bottom: 0.5rem;
    }
    
    .stMarkdown ul li::marker,
    .stMarkdown ol li::marker {
        color: #60a5fa !important;
    }
}

/* Progress bar styling */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent-secondary), var(--accent-primary));
    border-radius: 4px;
}

/* Better progress bar text */
@media (prefers-color-scheme: dark) {
    .stProgress .stMarkdown {
        color: #cbd5e1 !important;
    }
}

/* Spinner styling */
.stSpinner > div > div {
    border-color: var(--accent-primary);
    border-right-color: transparent;
    border-width: 3px;
}

/* Better spinner and loading text */
@media (prefers-color-scheme: dark) {
    .stSpinner + div {
        color: #cbd5e1 !important;
    }
}

/* Divider styling */
hr {
    border: none;
    height: 1px;
    background-color: var(--border-primary);
    margin: 2rem 0;
}

/* Download button special styling */
button[data-testid="stDownloadButton"] {
    background: linear-gradient(90deg, var(--accent-secondary), var(--accent-primary));
    color: white;
    border: none;
    font-weight: 600;
}

button[data-testid="stDownloadButton"]:hover {
    background: linear-gradient(90deg, var(--accent-primary), #0d7de8);
    transform: translateY(-1px);
}

/* Dataframe styling for dark mode */
.stDataFrame {
    background-color: var(--bg-secondary);
    color: var(--text-primary);
}

/* Enhanced table/dataframe readability */
@media (prefers-color-scheme: dark) {
    .stDataFrame,
    .stDataFrame table,
    .stDataFrame tbody,
    .stDataFrame thead,
    .stDataFrame tr,
    .stDataFrame td,
    .stDataFrame th {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border-color: #475569 !important;
    }
    
    .stDataFrame th {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
        font-weight: 600;
    }
    
    .stDataFrame tr:nth-child(even) {
        background-color: #0f172a !important;
    }
    
    .stDataFrame tr:hover {
        background-color: #334155 !important;
    }
}

/* Caption styling */
.stCaption {
    color: var(--text-tertiary) !important;
}

/* Enhanced caption and help text */
@media (prefers-color-scheme: dark) {
    .stCaption,
    caption,
    .caption {
        color: #94a3b8 !important;
        font-size: 0.875rem;
        opacity: 0.9;
    }
}

/* Info/warning/success boxes */
div[data-testid="stInfo"] {
    background-color: var(--bg-tertiary);
    color: var(--text-primary);
    border-left: 4px solid var(--accent-primary);
}

div[data-testid="stWarning"] {
    background-color: var(--bg-tertiary);
    color: var(--text-primary);
    border-left: 4px solid var(--warning);
}

div[data-testid="stSuccess"] {
    background-color: var(--bg-tertiary);
    color: var(--text-primary);
    border-left: 4px solid var(--success);
}

/* Enhanced sidebar text readability */
@media (prefers-color-scheme: dark) {
    .sidebar .stMarkdown h1,
    .sidebar .stMarkdown h2,
    .sidebar .stMarkdown h3,
    .sidebar .stMarkdown p,
    .sidebar .stMarkdown li,
    .sidebar .stMarkdown span,
    .sidebar div[data-testid="stText"] {
        color: #e2e8f0 !important;
    }
    
    .sidebar .stMetric label {
        color: #94a3b8 !important;
    }
    
    .sidebar .stMetric div[data-testid="metric-value"] {
        color: #f1f5f9 !important;
    }
}

/* Better contrast for disabled/readonly elements */
@media (prefers-color-scheme: dark) {
    textarea:disabled,
    input:disabled,
    select:disabled {
        background-color: #1e293b !important;
        color: #cbd5e1 !important;
        border-color: #475569 !important;
        opacity: 0.9 !important;
        -webkit-text-fill-color: #cbd5e1 !important;
    }
    
    /* Specific fix for Streamlit text areas */
    .stTextArea textarea:disabled {
        color: #cbd5e1 !important;
        -webkit-text-fill-color: #cbd5e1 !important;
        background-color: #1e293b !important;
    }
}

/* Responsive design */
@media (max-width: 768px) {
    .nav-container {
        padding: 0 1rem;
    }
    
    .nav-links {
        gap: 0.8rem;
    }
    
    .main .block-container {
        padding: 2rem 1.5rem;
        margin: 90px 1rem 1rem 1rem;
        border-radius: 12px;
    }
    
    .headline {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .subtext {
        font-size: 1rem;
        margin-bottom: 2rem;
    }
}

/* Focus indicators for accessibility */
button:focus,
input:focus,
textarea:focus,
select:focus {
    outline: 2px solid var(--accent-primary);
    outline-offset: 2px;
}

/* Loading animation */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.main .block-container {
    animation: fadeInUp 0.6s ease-out;
}

/* Force text colors for better visibility */
* {
    color: inherit;
}

/* Ensure all Streamlit elements respect dark mode */
@media (prefers-color-scheme: dark) {
    .stApp, .stApp > div, .main {
        background-color: var(--bg-primary) !important;
    }
    
    /* Force all text to be visible */
    .stMarkdown *, 
    .streamlit-expanderContent *,
    .stTextArea label,
    .stSelectbox label,
    .stFileUploader label,
    .stTextInput label,
    div[data-testid="stText"],
    p, span, div, li, h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }
    
    /* Specific fixes for common Streamlit elements */
    .stSelectbox div[data-baseweb="select"] {
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
    }
    
    .stTextInput input {
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
    }
    
    .stTextArea textarea {
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
    }
}

</style>
"""