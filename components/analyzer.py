from components.agents import Agent
from components.prompts.document_analyzer_prompt import DOCUMENT_ANALYZER_PROMPT

document_analyzer = Agent(
    name="Document Analyzer",
    instructions=DOCUMENT_ANALYZER_PROMPT
)
