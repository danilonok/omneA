from pydantic import BaseModel
from configs.llm_config import Settings
from typing import Type
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
class BaseGenerator:
    """Base generator wrapper class to generate text given prompt"""
    def __init__(self, prompt: str, model: str, output_model: Type[BaseModel]):
        self.prompt_str = prompt
        if model=='ollama':
            self.llm = Settings.llm
        else:
            self.llm = None
        assert self.llm, "LLM must be defined"
        self.output_model = output_model
    def generate(query: str):
        parser = LLMTextCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(self.output_model),
            prompt_template_str=self.prompt_str,
            llm=self.llm
        ) 
        response = parser(query=query)   
        return response
    def agenerate():
        pass