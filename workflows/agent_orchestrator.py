from platform import system

from llama_index.core.agent.workflow import FunctionAgent, ReActAgent
from configs.llm_config import Settings
from workflows.file_agent import file_agent

agent_orchestrator = ReActAgent(
    name='AgentOrchestrator',
    description='Used to orchestrate the whole multi-agent workflow. Can call another agents with Handoff function. DO NOT CALL TOOLS OF AGENTS! You can only handoff.',
    system_prompt=('You are AgentOrchestrator agent, which must orchestrate the whole agentic system. Can call another agents with Handoff function. DO NOT CALL TOOLS OF AGENTS!'
                   'When writing a final answer, do not make up results. If agentic system was unable to perform an action, be honest and ask the user to retry. You can only handoff.'),
    can_handoff_to=['FileAgent', 'PowershellAgent', 'RunAppAgent'],
)