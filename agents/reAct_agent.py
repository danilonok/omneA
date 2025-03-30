"""
Adaptation of famous reAct agent
"""

from llama_index.core import PromptTemplate

from agents.agent import Agent
from configs.llm_config import Settings
from tools.tool import Tool
from typing import List


ReActAgentPrompt = (
"Task: Answer the following question using the provided tools."
"You are able to use such tools:"
"{tools}"
"Format:"
"You should think aloud and reason step by step. After your reasoning (# Thought), specify an action (# Action) and provide the result of that action (# Observation). Continue this process until you arrive at the final answer."
"Example:"
"Query: What is the population of the largest city in France?"
"Thought: The largest city in France is Paris. I need to find the current population of Paris."
"Action: Tool(Search('current population of Paris'))"
"Observation: The population of Paris is approximately 2.1 million people."
"Thought: I have the information needed to answer the question."
"Final Answer: The population of the largest city in France, Paris, is approximately 2.1 million people."
"Tools syntax: ToolName(kwargs)"
"ALWAYS generate a command after Action"
"Use only available tools given to you."
"Query: {query_str}"
)
ReActAgentPrompt = PromptTemplate(ReActAgentPrompt)

class ReActAgent(Agent):
    def __init__(self, prompt: str=None, llm=None, tools: List[Tool]=None):
        super().__init__()
        self.prompt = prompt or ReActAgentPrompt
        self.llm = llm or Settings.llm
        self.tools = tools
    def generateToolsDescription(self):
        if self.tools:
            tools_description = ""
            for i, tool in enumerate(self.tools):
                tools_description += f'{i+1}. {tool.name} : {tool.description} \n Tool Syntax: {tool.syntax}\n'
            return tools_description
    def run(self, query: str):
        prompt = self.prompt.format(query_str=query, tools=self.generateToolsDescription())
        print(prompt)
        response = self.llm.complete(prompt)
        return response
