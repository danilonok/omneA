from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context
from tools.command_executor import execute_cmd_command
from workflows.powershell_command_generator import CommandGenerator

command_generator = CommandGenerator()

async def generate_command(ctx: Context, query: str):
    """Create a list of Powershell commands to fulfil the query. Your input should contain all information needed to generate a Powershell command using LLM."""
    generated_commands = command_generator.generate(query=query)
    return f'Generated Powershell command: {str(generated_commands)}'

async def execute_command(ctx: Context, command: str):
    """Useful for executing generated Powershell command in Windows 11 PC. Your input should contain a SINGLE properly syntaxed command."""
    return execute_cmd_command(command)

powershell_agent = FunctionAgent(
    name='PowershellAgent',
    description='Useful for creating and executing various Powershell commands in Windows 11. Can execute API calls, open Websites and other. It is very powerfull and can execute almost everything.',
    system_prompt=(
        "You are PowershellAgent that can create and execute Windows 11 Powershell Commands"
        "Given a request, you should fulfil it and provide concise response as a report of your work."
        "After you have completed your actions, handoff to AgentOrchestrator!"
        "Always return back to AgentOrchestrator. Be sure you finish with a handoff."
        "Always give a proper reason for a handoff. AgentOrchestrator must know exactly why."
    ),
    tools=[generate_command, execute_command],
    can_handoff_to=['AgentOrchestrator']
)