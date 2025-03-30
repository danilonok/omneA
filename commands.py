from typing import List
from pydantic import BaseModel, Field
from configs.llm_config import llm


class Command(BaseModel):
    """Class Representing CMD Command to fulfil the step"""
    text: str = Field(description="Full text of proper-syntaxed CMD command")

class Commands(BaseModel):
    """All commands to fulfil the step"""
    commands: List[Command]

from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser


prompt_template_str = """\
Given a current step to fulfil the query, you must generate proper-syntaxed CMD commands for the system to execute. You won't receive any responses till all commands are executed.
Always generate one command at the time - no && operator allowed!
Query:
{query}
Step:
{step}
Previous step and its result(sometimes just th error of the same step - try to fix it!):
{prev_step_result}
"""

commands_parser = LLMTextCompletionProgram.from_defaults(
    output_parser=PydanticOutputParser(Commands),
    prompt_template_str=prompt_template_str,
    llm=llm
)
