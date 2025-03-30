"""
Defines a basic completion agent
"""

from agents.agent import Agent
from configs.llm_config import Settings
from prompts.prompts import default_completion_prompt

class CompletionAgent(Agent):
    """
    Simple completion agent, which is capable of generating text given a prompt.
    """



    def __init__(self, prompt: str=None, llm=None):
        super().__init__()
        self.prompt = prompt or default_completion_prompt
        self.llm = llm or Settings.llm

    def run(self, query: str):
        """Takes query and generates a response"""
        response = self.llm.complete(self.prompt.format(query_str=query))
        return response


