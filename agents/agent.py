"""
Defines a base agent
"""

from abc import ABC, abstractmethod
from llama_index.core.agent import ReActAgent

class Agent(ABC):
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = self.__class__.__doc__

    @abstractmethod
    def run(self, query: str):
        pass