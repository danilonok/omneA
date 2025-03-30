from typing import List
from pydantic import BaseModel, Field
from configs.llm_config import llm
class Step(BaseModel):
    """Class Representing Step to resolve user's issue"""
    text: str = Field(description="Text explanation of a step to resolve user's request")

class Steps(BaseModel):
    """All steps to resolve user's issue"""
    steps: List[Step]


from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser

prompt_template_str_first_try = """\
Given a user's query generate a numbered list with all necessary steps to fulfill user request using only Windows 11 CMD Console. You should not write the commands themselves.
You write these steps for a system, that generates the commands and executes them, not for a human. The environment is already set, so there is no need to open CMD Shell.
User's request:
{query}
Before giving the numbered list of steps required to fulfil user's request, do thinking process - write down your thougths on how you would divide this task.
Output Format:
### Thinking
% your thoughts here %
### Steps 
% steps %
"""




steps_parser = LLMTextCompletionProgram.from_defaults(
    output_parser=PydanticOutputParser(Steps),
    prompt_template_str=prompt_template_str_first_try,
    llm=llm
)