from llama_index.core.agent.workflow import FunctionAgent, ReActAgent
from configs.llm_config import Settings
from workflows.file_agent import file_agent

agent_orchestrator = ReActAgent(
    name='AgentOrchestrator',
    description='Used to orchestrate the whole multi-agent workflow. Can call another agents.',
    can_handoff_to=['FileAgent', 'PowershellAgent'],
)