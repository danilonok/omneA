"""
ReActAgent parser module. Parses the responses of the LLM
"""

from tools.tool import Tool
from typing import List

import re

class Parser:
    def __init__(self, tools: List[Tool]):
        self.tools = tools

    def parse(self, query: str):
        match = re.findall(r'FS_TOOL\(([^)]+)\)', query)
        # divide args
        args = match[0].split(", ")
        args = [arg.replace('\'', '') for arg in args]
        # clear it from quotes

        print(args)

