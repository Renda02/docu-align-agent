from components.agents import Agent
from components.prompts.style_enforcer_prompt import STYLE_ENFORCER_PROMPT

style_enforcer = Agent(
    name="Style Enforcer",
    instructions=STYLE_ENFORCER_PROMPT
)