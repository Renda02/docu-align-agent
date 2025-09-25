# A multiline string containing all the custom CSS for the Streamlit app.
# The CSS is injected directly into the app using st.markdown.
CUSTOM_CSS = """
<style>
/* Main container styling */
.stApp {
    background-color: #f0f2f6; /* A light, soft gray background */
    color: #333; /* Dark gray text for readability */
    font-family: 'Segoe UI', 'Roboto', sans-serif;
}

/* Page title and headers */
h1 {
    color: #004d40; /* A dark teal color for the main title */
    font-size: 2.5em;
    font-weight: 600;
    text-align: center;
    margin-bottom: 20px;
}

h3 {
    color: #00695c; /* A slightly lighter teal for subheadings */
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 5px;
    margin-top: 30px;
}

/* Text areas for input */
.stTextArea label {
    font-weight: bold;
    color: #444;
}

.stTextArea > div > div > textarea {
    border-radius: 10px;
    border: 1px solid #ccc;
    padding: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: box-shadow 0.3s ease-in-out;
}

.stTextArea > div > div > textarea:focus {
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* File uploader styling */
.stFileUploader label {
    font-weight: bold;
    color: #444;
}

.stFileUploader > div > div {
    border-radius: 10px;
    border: 1px solid #ccc;
    padding: 10px;
    background-color: #fff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

/* Buttons */
.stButton > button {
    background-color: #00796b; /* A vibrant teal for buttons */
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0,0,0,0.15);
}

/* Alert boxes (info, success, warning, error) */
.stAlert {
    border-radius: 10px;
    padding: 15px;
    margin-top: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.stAlert.success {
    background-color: #e8f5e9;
    color: #2e7d32;
    border-left: 5px solid #4caf50;
}
.stAlert.info {
    background-color: #e3f2fd;
    color: #1976d2;
    border-left: 5px solid #2196f3;
}
.stAlert.warning {
    background-color: #fffde7;
    color: #f9a825;
    border-left: 5px solid #ffc107;
}

/* Markdown blocks */
.markdown-text-container blockquote {
    background-color: #f5f5f5;
    border-left: 5px solid #bdbdbd;
    padding: 10px 15px;
    border-radius: 5px;
    margin-left: 0;
}

/* Spinner */
.stSpinner > div > div {
    border-width: 4px;
    border-color: #00796b;
    border-right-color: transparent;
}
</style>
"""
