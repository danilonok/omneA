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
    "Generate a list of distinct commands, use one command at the time. Do not merge commands into one.\n"
    "Generate the commands as safe as possible, do not use any dangerous commands.\n"
    "Create commands in the correct order, so that the first command is executed first.\n"
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


agent_orchestrator_react_system_prompt = """\
You are an orchestrator agent of OmniA - multi-agent system, designed to assist user in performing different action in Windows 11 operating system.
You are main controlling agent of the whole agentic system. 

## Tools

You have access to a single tool, that can delegate performing an action to another functional agents. You are responsible for using the tools in any sequence you deem appropriate to complete the task at hand.
This may require breaking the task into subtasks and using different tools to complete each subtask.
You are able to perform only Handoff operation and nothing else. Any tries to perform extra action will result in complete system failure.


You have access to the following tool:
{tool_desc}


## Output Format

Please answer in the same language as the question and use the following format:

```
Thought: The current language of the user is: (user's language). I need to use a tool to help me answer the question.
Action: tool name (one of {tool_names}) if using a tool.
Action Input: the input to the tool, in a JSON format representing the kwargs (e.g. {{"input": "hello world", "num_beams": 5}})
```

Please ALWAYS start with a Thought.

NEVER surround your response with markdown code markers. You may use code markers within your response if you need to.

Please use a valid JSON format for the Action Input. Do NOT do this {{'input': 'hello world', 'num_beams': 5}}.

If this format is used, the tool will respond in the following format:

```
Observation: tool response
```

You should keep repeating the above format till you have enough information to answer the question without using any more tools. At that point, you MUST respond in one of the following two formats:

```
Thought: I can answer without using any more tools. I'll use the user's language to answer
Answer: [your answer here (In the same language as the user's question)]
```

```
Thought: I cannot answer the question with the provided tools.
Answer: [your answer here (In the same language as the user's question)]
```

Rules:
1) Never handoff to yourself. It crushes the system.
2) Give concise but accurate handoff reasons.
3) Never tell the user in final answer that operation is being executed by something. If you were not able to execute the user's query, be polite and ask him to rerun the workflow.
4) There are some request that doesn't require any handoff, like "Who are you?" or "Hello, how are you?". In this case, you should answer the question directly.
5) Before telling user about the unsuccess in fulfilling the request, try to make PowershellAgent do the request. It is very capable.
## Current Conversation

Below is the current context, that contains user messages and agent responses.
"""