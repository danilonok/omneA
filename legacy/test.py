from llama_index.core.prompts import PromptTemplate

from agents.reAct_agent import ReActAgent
from legacy.file_system_tool import FileSystemTool
from agents.parser import Parser

fs_tool = FileSystemTool()

print(fs_tool.description)

PROMPT = (
    "You are Windows Assistant, that fulfils user's requests."
    "You are able to use such tools:"
    "{tools}"
    "To call tools always put a command into ``` quotes."
    "Query:"
    "{query_str}"

)
prompt = PromptTemplate(PROMPT)

parser = Parser(tools=[fs_tool])

print(parser.parse("FS_TOOL(copy, 'C:/Work/report.txt', 'D:/Backup')"))

# response = llm.complete(prompt.format(query_str="Copy file C:/Work/report.txt to D:/Work/reports/",
#                     tools=f"{fs_tool.name}: {fs_tool.description}.\n It has such syntax: {fs_tool.syntax}"))

# comp_agent = CompletionAgent()
#
# response = comp_agent.run("Who is Ariana Grande?")


react_agent = ReActAgent(tools=[fs_tool])

response = react_agent.run("Copy my file C:/Work/report.txt to D:/Backup")


print(response)

