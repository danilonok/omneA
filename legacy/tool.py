from abc import ABC, abstractmethod
"""
Represents the tool concept - agent usable solution
"""

class Tool(ABC):
    """
    Base tool class
    """
    syntax: str = ""
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = self.__class__.__doc__

    @abstractmethod
    def execute(self, command: str):
        pass


