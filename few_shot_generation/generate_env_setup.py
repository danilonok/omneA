from core.generator import BaseGenerator
from core.prompts.prompts import DEFAULT_ENV_SETUP_COMMANDS_TMPL
from pydantic import BaseModel
from typing import List, Optional
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from retry import retry

class Command(BaseModel):
    """Data model for a powershell command to execute in operating system"""
    command: str

class Commands(BaseModel):
    """Data model for a list of powershell commands to execute in operating system"""
    commands: List[Command]

class EnvSetupGenerator(BaseGenerator):
    def __init__(self, prompt: Optional[str] = None, model: Optional[str] = None, output_model: Optional[BaseModel] = None) -> List[Command]:
        super().__init__(prompt=DEFAULT_ENV_SETUP_COMMANDS_TMPL, model='ollama', output_model=Commands)
    
    @retry(delay=1)
    def generate(self, query: str, commands: List[str]) -> List[Command]:
        parser = LLMTextCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(self.output_model),
            prompt_template_str=self.prompt_str,
            llm=self.llm
        ) 
        response = parser(query=query, commands=commands)
        return response.commands
