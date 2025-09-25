# Docu-Align App: The Automated Documentation Assistant

**Docu-Align App** is a Streamlit-based application designed to streamline the documentation process.  
It uses a series of LLM agents to analyze existing documents and enforce a consistent style on new, incoming content—ensuring all your documentation is aligned and polished.

---

## ✨ Key Features

- **Document Analysis**: Analyze existing documentation to identify key styles, tones, and content gaps.  
- **Style Enforcement**: Automatically rewrite new content to match the established style and tone of your existing documents.  
- **User-Friendly Interface**: A clean and modern web interface built with Streamlit for easy file uploads and content management.  
- **Modular Design**: A well-structured codebase that separates agents, prompts, and UI components for easy maintenance and scalability.  

---

## 📂 Project Structure
The project is organized into a modular folder structure to keep the codebase clean and manageable:

```
/docu-align-app
|-- documentation_app.py      # Main Streamlit application file
|-- README.md                 # Project documentation
|-- .env                      # Environment variables for API keys
|
|-- /components               # Contains all agent-related logic
|   |-- __init__.py
|   |-- agents.py             # Agent and Runner class definitions
|   |-- prompts.py            # Agent prompt instructions
|   |-- analyzer.py           # The Document Analyzer agent
|   |-- enforcer.py           # The Style Enforcer agent
|
|-- /style                    # Contains UI and styling files
|   |-- __init__.py
|   |-- style.py              # Custom CSS for the Streamlit UI
```

---

## 🚀 Getting Started

Follow these steps to set up and run the application on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/docu-align-app.git
cd docu-align-app
```

### 2. Create the `.env` File
Create a file named `.env` in the root directory of your project and add your OpenAI API key:

```env
OPENAI_API_KEY="your_actual_api_key_here"
```

### 3. Install Required Libraries
From your terminal, install the necessary Python libraries:

```bash
pip install streamlit python-dotenv openai
```

### 4. Run the Application
Once everything is set up, launch the app with:

```bash
streamlit run documentation_app.py
```

The application will open in your default web browser.

---

## ⚙️ How It Works

1. **User Input**: The user uploads or pastes two pieces of content:  
   - a document to analyze  
   - a new piece of content to be styled  

2. **Orchestration**: `documentation_app.py` orchestrates the workflow, calling the agents in a sequence.  

3. **Agent 1 – Document Analyzer**:  
   Analyzes the existing document’s style and tone based on instructions in `prompts.py`.  

4. **Agent 2 – Style Enforcer**:  
   Uses the analysis from the first agent to rewrite the new content, ensuring it conforms to the identified style.  

5. **Output**: The final, polished document is displayed to the user in the Streamlit UI.  

---
