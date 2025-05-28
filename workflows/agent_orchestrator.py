from platform import system

from llama_index.core.agent.workflow import FunctionAgent, ReActAgent
from core.prompts.prompts import agent_orchestrator_react_system_prompt

agent_orchestrator = ReActAgent(
    name='AgentOrchestrator',
    description='Used to orchestrate the whole multi-agent workflow. Can call another agents with Handoff function. DO NOT CALL TOOLS OF AGENTS! You can only handoff.',
    system_prompt=('You are AgentOrchestrator agent, which must orchestrate the whole agentic system. Can call another agents with Handoff function. DO NOT CALL TOOLS OF AGENTS!'
                   'When writing a final answer, do not make up results. If agentic system was unable to perform an action, be honest and ask the user to retry. You can only handoff.\n'
                   'YOU ARE ALLOWED TO USE ONLY HANDOFF TOOL. YOU WILL BE PUNISHED IF YOU USE ANY OTHER!'),
    can_handoff_to=['FileAgent', 'PowershellAgent', 'RunAppAgent', 'WebSearchAgent'],
)

agent_orchestrator.update_prompts({"react_header": agent_orchestrator_react_system_prompt})