import streamlit as st
from openai import OpenAI
import os

# Define a class for an Agent. It's a simple data structure to hold the name, instructions, and model.
class Agent:
    def __init__(self, name: str, instructions: str, model: str = "gpt-3.5-turbo"):
        self.name = name
        self.instructions = instructions
        self.model = model  # Add model parameter with default fallback

# This is your LLM runner that now supports different models per agent.
class Runner:
    def __init__(self, api_key: str):
        self.api_key = api_key
        print("Runner initialized with API key.")

    async def run(self, agent, user_input):
        print(f"--- Running Agent: {agent.name} with model: {agent.model} ---")
        
        # Make API call using the agent's specified model
        client = OpenAI(api_key=self.api_key)
        try:
            response = client.chat.completions.create(
                model=agent.model,  # Use agent's specified model
                messages=[
                    {"role": "system", "content": agent.instructions},
                    {"role": "user", "content": user_input}
                ]
            )
            final_output = response.choices[0].message.content
        except Exception as e:
            final_output = f"API call failed with {agent.model}: {e}"

        return MockResult(final_output)
        
# A simple class to simulate the result object from an LLM API call.
class MockResult:
    def __init__(self, final_output):
        self.final_output = final_output