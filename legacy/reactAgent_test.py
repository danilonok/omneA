
from llama_index.core.agent.workflow import ReActAgent


from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from tools import command_executor
from legacy import popup
from llama_index.core import PromptTemplate
from index_loader.load_index import index
from llama_index.tools.wikipedia.base import WikipediaToolSpec
from llama_index.core.tools.tool_spec.load_and_search import (
    LoadAndSearchToolSpec,
)

new_summary_tmpl_str = (
    "Helpful powershell command that can be handy:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "You are Generator of Windows 11 Powershell commands."
    "Given users request you must return just one single command\n"
    "You can generate only one-line command.\n"
    "Do not use any external software or try to install it."
    "Query: {query_str}\n"
    "Powershell Command: "
)
new_summary_tmpl = PromptTemplate(new_summary_tmpl_str)



engine = index.as_query_engine(similarity_top_k=3)
engine.update_prompts(
    {"response_synthesizer:summary_template": new_summary_tmpl}
)


pc_assistant_agent_prompt_template="""
You are a helpful Windows 11 PC Assistant, that must fulfil the request.
Never give up on trying, user cannot do it without your help.

Never generate commands yourself, you have a tool for that. It knows better.

All text assignments - as summarization, generation, rewriting - it is your task, do not use tools for that.

If you think there is not enough context information to fulfil the request, reask the user.

If you received a command to open a file, it means you should read its content
## Tools

You have access to a wide variety of tools. You are responsible for using the tools in any sequence you deem appropriate to complete the task at hand.
This may require breaking the task into subtasks and using different tools to complete each subtask.

You have access to the following tools:
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

## Current Conversation

Below is the current conversation consisting of interleaving human and assistant messages.
"""
pc_assistant_agent_prompt = PromptTemplate(pc_assistant_agent_prompt_template)




react_agent_prompt_template="""
You are a helpful assistant, that must fulfil the request.
User is not able to help himself, you should do all the actions.

All text assignments - as summarization, generation, rewriting - it is your task, do not use tools for that.
The computer tasks should be done with another agent(tool).

To show information to user, use tools.

You should not use tools if you can omit it. If you have general knowledge about the question (like what is 2 plus 2), you should answer yourself.
The Tools and Agents you call do not have access to your messages. You should always provide context when calling a tool.
## Tools

You have access to a wide variety of tools. You are responsible for using the tools in any sequence you deem appropriate to complete the task at hand.
This may require breaking the task into subtasks and using different tools to complete each subtask.

You have access to the following tools:
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

## Current Conversation

Below is the current conversation consisting of interleaving human and assistant messages.
"""
react_agent_prompt = PromptTemplate(react_agent_prompt_template)


tool1 = QueryEngineTool(query_engine=engine,
        metadata=ToolMetadata(
            name="cmd_exec",
            description=(
                "Executes Windows CMD commands and returns their output."
                "Executes one command in a time"
                "Use Windows 11 CMD command as input to the tool."
                'Input format: {"command": "powershell Command Args"}'
                "When you got a generated command, pass it to this tool"

            )))
powershell_generator_tool = QueryEngineTool(query_engine=engine,
        metadata=ToolMetadata(
            name="powershell_command_generator",
            description=(
                "Generates Windows Powershell commands. Gives the most possible command given request."
                "Generates one command in a time"
                "Use detailed query of the request as input to the tool."
                "Its output should be used in cmd_exec tool"
                "Never pass the command itself, only instruction"
            )))
executor_tool = FunctionTool.from_defaults(fn=command_executor.execute_cmd_command, name="cmd_executor",
        description="Executes Windows CMD commands and returns their output.")
popup_tool = FunctionTool.from_defaults(fn=popup.show_popup, name="popup", description="Shows a popup window with the given text.")

tools_1 = [powershell_generator_tool, executor_tool]
agent_1 = ReActAgent(
    name="pc_assistant",
    description="A helpful assistant that can perform actions with the user's PC.",
    tools=tools_1,
        # context=context
)
agent_1.update_prompts({"react_header": pc_assistant_agent_prompt})


async def call_pc_assistant_agent(input: str):
    """An ReAct-agent that can perform actions with the user's PC.
        Use detailed request(plain text of what should be done) as an input to the tool.
        Always pass ALL information in input field!
        Example: {"input": "Open browser"}
        Example: {"input": "Open file, path: path/to/file"}"""

    handler = agent_1.run(input)
    return await handler

pc_assistant_tool = FunctionTool.from_defaults(
    fn=call_pc_assistant_agent,
    name="pc_assistant_agent",
    description=("An agent that can perform actions with the user's PC. Pass the request as a string.")
)

wiki_spec = WikipediaToolSpec()
# Get the search wikipedia tool
wiki_tool = wiki_spec.to_tool_list()[1]
wiki_tool = LoadAndSearchToolSpec.from_defaults(wiki_tool).to_tool_list()
tools_2 = [pc_assistant_tool, popup_tool] + wiki_tool

agent_2 = ReActAgent(
    tools=tools_2,
    max_iterations=20,
    name="react_agent",
    description="An ReAct-agent that can perform actions with the user's PC.",
    # context=context
)
agent_2.update_prompts({"react_header": react_agent_prompt})

#response = agent_2.chat("Request: Summarize contents of file C:/Work/day_report.txt and write this summary to file day_report_summary.txt in the same folder")
# response = agent_2.chat("Write a story about robotic pony into C:/Work/robopony.txt")
# response = agent_2.chat("Create a simple python script that calculates Fibonacci number and execute it")
# print(str(response))