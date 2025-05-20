from llama_index.core.prompts import PromptTemplate

DEFAULT_TASK_GENERATION_TMPL = (
    "You must create {num_tasks}  unique and original queries tasks that can be performed within Windows 11 operating system\n"

    "Your job is to generate a list of diverse, unique, and useful natural language queries. Each one should describe a specific goal the user wants to accomplish on their PC, using PowerShell."
    "Guidelines:\n"
    "- Write **natural, human-like** queries.\n"
    "- Cover a **variety of topics**, like file operations, service management, performance, system settings, etc.\n"
    "- Avoid duplicates or overly similar queries.\n"
    "- Keep each query to **1–2 concise sentences**.\n"
    "- Do **not** include explanations, comments, or commands — just the queries.\n"
    "Examples (do NOT repeat or base output directly on these):\n"
    "- List all .mp3 files in my Music folder.\n"
    "- Check if Windows Update is running.\n"
    "- Compress all the PDFs in the Reports folder into a zip archive.\n"
    
    "It should be possible to execute them using Powershell."
    "The task must be as if the real PC user would ask for it.\n"
    "The created tasks must be very specific and realistic.\n"
    "Do not create any tasks that cannot be fully executed using Powershell."
)


DEFAULT_COMMAND_GENERATION_TMPL = (
    "You must create all required powershell commands to execute the user query {query}\n"
    "Generate a list of distict commands, use one command at the time. Do not merge commands into one.\n"
    "Generate the commands as safe as possible, do not use any dangerous commands.\n"
    "Create commands in the correfct order, so that the first command is executed first.\n"
    "Do not use any comments in the commands.\n"
    "Do not use any unnecessary commands.\n"
)

DEFAULT_ENV_SETUP_COMMANDS_TMPL = (
    "You must create all required powershell commands to populate a Windows 11 PC to test the execution of the user query: {query}\n"
    "The following commands will be tested: \n"
    "{commands}"
    "You should create all listed files, folders."
    "Generate a list of distict commands, use one command at the time. Do not merge commands into one.\n"
)