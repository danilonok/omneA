from llama_index.core.prompts import PromptTemplate

DEFAULT_TASK_GENERATION_TMPL = (
    "You must create {num_tasks} comlex tasks that can be performed within Windows 11 operating system\n"
    "It should be possible to execute them using Powershell. They must be complex enough to execute them in at least two steps."
    "The task must be as if the real PC user would ask for it.\n"
)
