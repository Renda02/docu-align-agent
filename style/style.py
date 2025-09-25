# Modern clean styling for Docu-Align App
CUSTOM_CSS = """
<style>
/* Import Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Navigation header styling */
.nav-header {
    background-color: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    padding: 1rem 0;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
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
    background: linear-gradient(135deg, #40bfff, #1a9cff);
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
    color: #1f2937;
    letter-spacing: -0.02em;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.nav-link {
    color: #6b7280;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s ease;
    cursor: pointer;
}

.nav-link:hover {
    color: #1a9cff;
}

.nav-signin {
    background: linear-gradient(90deg, #40bfff, #1a9cff);
    color: white !important;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
    text-decoration: none;
}

.nav-signin:hover {
    background: linear-gradient(90deg, #1a9cff, #0d7de8);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(26, 156, 255, 0.3);
    color: white !important;
}

/* Global styling */
.stApp {
    background-color: #fafafa;
    font-family: "Inter", sans-serif;
}

/* Hide Streamlit default header */
header[data-testid="stHeader"] {
    display: none;
}

/* Ensure body and app have no default margin/padding */
.stApp {
    padding-top: 0;
    margin-top: 0;
}

/* Main container styling */
.main .block-container {
    background-color: white;
    padding: 3rem 2.5rem;
    border-radius: 16px;
    margin: 80px auto 2rem auto;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 15px rgba(0, 0, 0, 0.1);
    max-width: 900px;
    border: 1px solid #e5e7eb;
}

/* Sidebar styling */
.sidebar .block-container {
    background-color: white;
    border-radius: 12px;
    margin: 1rem;
    padding: 2rem 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border: 1px solid #e5e7eb;
}

/* Modern headline styling */
.headline {
    text-align: center;
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 2.4rem;
    font-weight: 700;
    color: #1f2937;
    line-height: 1.2;
}

.headline .highlight {
    color: #1a9cff;
}

/* Subtext styling */
.subtext {
    text-align: center;
    color: #6b7280;
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
    color: #1f2937;
    line-height: 1.2;
}

h2 {
    color: #374151;
    font-weight: 600;
    font-size: 1.5rem;
    margin: 2rem 0 1rem 0;
    border-bottom: 2px solid #f3f4f6;
    padding-bottom: 0.5rem;
}

h3 {
    color: #4b5563;
    font-weight: 600;
    font-size: 1.25rem;
    margin: 1.5rem 0 1rem 0;
}

/* Input styling */
.stTextInput > div > div > input {
    border-radius: 10px;
    border: 1px solid #d1d5db;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    color: #374151;
    background-color: white;
    transition: all 0.2s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #1a9cff;
    box-shadow: 0 0 0 3px rgba(26, 156, 255, 0.1);
    outline: none;
}

.stSelectbox > div > div > div {
    border-radius: 10px;
    border: 1px solid #d1d5db;
    padding: 0.5rem;
    background-color: white;
    color: #374151;
    transition: all 0.2s ease;
}

.stSelectbox > div > div > div:focus {
    border-color: #1a9cff;
    box-shadow: 0 0 0 3px rgba(26, 156, 255, 0.1);
}

/* Text area styling */
.stTextArea > div > div > textarea {
    border-radius: 10px;
    border: 1px solid #d1d5db;
    padding: 1rem;
    font-size: 1rem;
    color: #374151;
    background-color: white;
    line-height: 1.5;
    transition: all 0.2s ease;
}

.stTextArea > div > div > textarea:focus {
    border-color: #1a9cff;
    box-shadow: 0 0 0 3px rgba(26, 156, 255, 0.1);
    outline: none;
}

/* Labels */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stFileUploader label {
    font-weight: 600;
    color: #374151;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}

/* Upload box styling */
.upload-box {
    border: 2px dashed #d0d7de;
    border-radius: 12px;
    padding: 2.5rem;
    text-align: center;
    background: white;
    margin: 1.5rem 0;
    transition: all 0.3s ease;
}

.upload-box:hover {
    border-color: #1a9cff;
    background-color: #f8faff;
}

.upload-help {
    color: #6b7280;
    margin-top: 12px;
    font-size: 0.95rem;
}

/* File uploader styling */
.stFileUploader {
    border: 2px dashed #d0d7de;
    border-radius: 12px;
    padding: 2.5rem;
    text-align: center;
    background: white;
    margin: 1.5rem 0;
    transition: all 0.3s ease;
}

.stFileUploader:hover {
    border-color: #1a9cff;
    background-color: #f8faff;
}

.stFileUploader label {
    color: #374151;
    font-weight: 500;
}

/* Button styling */
.stButton > button {
    border-radius: 12px;
    background: linear-gradient(90deg, #40bfff, #1a9cff);
    color: white;
    font-weight: 600;
    height: 3.5rem;
    font-size: 1.1rem;
    border: none;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(26, 156, 255, 0.3);
    padding: 0 2rem;
    width: 100%;
    margin: 1rem 0;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1a9cff, #0d7de8);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(26, 156, 255, 0.4);
}

.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 4px 12px rgba(26, 156, 255, 0.3);
}

/* Primary button enhanced styling */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(90deg, #40bfff, #1a9cff) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    height: 3.5rem !important;
    font-size: 1.1rem !important;
    box-shadow: 0 4px 12px rgba(26, 156, 255, 0.3) !important;
    width: 100% !important;
    margin: 1rem 0 !important;
    padding: 0 2rem !important;
}

button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(90deg, #1a9cff, #0d7de8) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(26, 156, 255, 0.4) !important;
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
    background: linear-gradient(90deg, #40bfff, #1a9cff) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(26, 156, 255, 0.3) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    display: block !important;
}

.analyze-button button:hover {
    background: linear-gradient(90deg, #1a9cff, #0d7de8) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(26, 156, 255, 0.4) !important;
}

.analyze-button button:active {
    transform: translateY(0) !important;
    box-shadow: 0 4px 12px rgba(26, 156, 255, 0.3) !important;
}

/* Secondary button styling */
.stButton > button[kind="secondary"] {
    background: white;
    color: #1a9cff;
    border: 2px solid #1a9cff;
    font-weight: 600;
}

.stButton > button[kind="secondary"]:hover {
    background: #f0f9ff;
    border-color: #0d7de8;
    color: #0d7de8;
}

/* Alert styling */
div[data-testid="stNotification"] {
    border-radius: 10px;
    border: none;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    font-weight: 500;
}

div[data-testid="stNotification"][data-color="success"] {
    background-color: #f0fdf4;
    color: #166534;
    border-left: 4px solid #22c55e;
}

div[data-testid="stNotification"][data-color="info"] {
    background-color: #eff6ff;
    color: #1e40af;
    border-left: 4px solid #3b82f6;
}

div[data-testid="stNotification"][data-color="warning"] {
    background-color: #fffbeb;
    color: #92400e;
    border-left: 4px solid #f59e0b;
}

div[data-testid="stNotification"][data-color="error"] {
    background-color: #fef2f2;
    color: #dc2626;
    border-left: 4px solid #ef4444;
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    color: #374151;
    font-weight: 500;
    padding: 0.75rem 1rem;
    transition: all 0.2s ease;
}

.streamlit-expanderHeader:hover {
    background-color: #f3f4f6;
    border-color: #d1d5db;
}

.streamlit-expanderContent {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 1rem;
}

/* Chat interface styling */
.stChatMessage {
    background-color: white;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 1rem 0;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.stChatMessage[data-testid="chat-message-user"] {
    background-color: #f0f9ff;
    border-color: #bfdbfe;
}

.stChatMessage[data-testid="chat-message-assistant"] {
    background-color: #f9fafb;
    border-color: #e5e7eb;
}

/* Progress bar styling */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #40bfff, #1a9cff);
    border-radius: 4px;
}

/* Spinner styling */
.stSpinner > div > div {
    border-color: #1a9cff;
    border-right-color: transparent;
    border-width: 3px;
}

/* Divider styling */
hr {
    border: none;
    height: 1px;
    background-color: #e5e7eb;
    margin: 2rem 0;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #f9fafb;
    padding: 0.25rem;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #6b7280;
    border-radius: 6px;
    font-weight: 500;
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background-color: white;
    color: #1a9cff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Metric styling */
div[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* Code block styling */
.stCode {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

/* Markdown styling */
.stMarkdown {
    color: #374151;
    line-height: 1.6;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #1f2937;
}

.stMarkdown blockquote {
    background-color: #f8fafc;
    border-left: 4px solid #cbd5e0;
    padding: 0.5rem 1rem;
    margin: 1rem 0;
    border-radius: 0 4px 4px 0;
}

/* Download button special styling */
button[data-testid="stDownloadButton"] {
    background: linear-gradient(90deg, #40bfff, #1a9cff);
    color: white;
    border: none;
    font-weight: 600;
}

button[data-testid="stDownloadButton"]:hover {
    background: linear-gradient(90deg, #1a9cff, #0d7de8);
    transform: translateY(-1px);
}

@media (max-width: 480px) {
    .nav-container {
        padding: 0 1rem;
    }
    
    .nav-links {
        gap: 0.5rem;
    }
    
    .nav-link {
        font-size: 0.8rem;
    }
    
    /* Hide Features and Pricing on very small screens */
    .nav-link:nth-child(1), /* Features */
    .nav-link:nth-child(2) { /* Pricing */
        display: none;
    }
    
    .nav-signin {
        padding: 0.4rem 0.6rem;
        font-size: 0.8rem;
    }
    
    .nav-title {
        font-size: 1rem;
    }
    
    .nav-logo {
        width: 28px;
        height: 28px;
        font-size: 0.9rem;
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
    
    .nav-link {
        font-size: 0.85rem;
        padding: 0.3rem 0;
    }
    
    .nav-signin {
        padding: 0.5rem 0.8rem;
        font-size: 0.85rem;
    }
    
    .nav-title {
        font-size: 1.15rem;
    }
    
    .nav-logo {
        width: 32px;
        height: 32px;
        font-size: 1rem;
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
    
    .stButton > button {
        height: 3rem !important;
        font-size: 1rem !important;
    }
    
    .analyze-button button {
        height: 3rem !important;
        font-size: 1rem !important;
    }
}

/* Focus indicators for accessibility */
button:focus,
input:focus,
textarea:focus,
select:focus {
    outline: 2px solid #1a9cff;
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

/* Add to your existing CUSTOM_CSS */

/* Dashboard text consistency */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #1f2937 !important;
}

.stMarkdown p, .stMarkdown li {
    color: #374151 !important;
    font-size: 1rem !important;
}

/* Metric styling */
div[data-testid="metric-container"] label {
    color: #6b7280 !important;
    font-size: 0.875rem !important;
}

div[data-testid="metric-container"] div[data-testid="metric-value"] {
    color: #1f2937 !important;
    font-size: 1.875rem !important;
    font-weight: 600 !important;
}

</style>
"""