from components.agents import Agent
from components.prompts.style_enforcer_prompt import STYLE_ENFORCER_PROMPT

style_enforcer = Agent(
    name="Style Enforcer",
    instructions=STYLE_ENFORCER_PROMPT,
    model="gpt-3.5-turbo"  # Keep cheaper model for style tasks
)