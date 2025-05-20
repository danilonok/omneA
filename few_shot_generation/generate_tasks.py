from core.generator import BaseGenerator
from core.prompts.prompts import DEFAULT_TASK_GENERATION_TMPL
from pydantic import BaseModel
from typing import List, Optional
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from retry import retry


class Task(BaseModel):
    """Data model for a task to execute in operating system"""
    task: str

class Tasks(BaseModel):
    """Data model for a list of tasks to execute in operating system"""
    tasks: List[Task]


class TaskGenerator(BaseGenerator):
    def __init__(self, prompt: Optional[str] = None, model: Optional[str] = None, output_model: Optional[BaseModel] = None) -> List[Task]:
        super().__init__(prompt=DEFAULT_TASK_GENERATION_TMPL, model='ollama', output_model=Tasks)

    @retry(delay=1)
    def generate(self, num_tasks):
        parser = LLMTextCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(self.output_model),
            prompt_template_str=self.prompt_str,
            llm=self.llm
        ) 
        
        response = parser(num_tasks=num_tasks)
        

        if len(response.tasks) != num_tasks:
            print(f"WARNING: Expected {num_tasks} tasks, but got {len(response.tasks)}")
        return response.tasks
        


