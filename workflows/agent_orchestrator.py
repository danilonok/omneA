from llama_index.core.agent.workflow import ReActAgent

agent_orchestrator = ReActAgent(
    name='AgentOrchestrator',
    description='Used to orchestrate the whole multi-agent workflow. Can call another agents with Handoff function. DO NOT CALL TOOLS OF AGENTS! You can only handoff.',
    can_handoff_to=['FileAgent', 'PowershellAgent', 'RunAppAgent', 'WebSearchAgent', 'MediaControlAgent'],
)
