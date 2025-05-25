
from llama_index.core.agent.workflow import AgentWorkflow
from configs.llm_config import Settings
from workflows.file_agent import file_agent
from workflows.powershell_agent import powershell_agent
from workflows.agent_orchestrator import agent_orchestrator
import os
info = {
    "User name": os.getenv("USERNAME"),
    "Computer name": os.getenv("COMPUTERNAME"),
    "User domain": os.getenv("USERDOMAIN"),
    "User profile": os.getenv("USERPROFILE"),
    "Home drive": os.getenv("HOMEDRIVE"),
    "Home path": os.getenv("HOMEPATH"),
    "APPDATA": os.getenv("APPDATA"),
    "LOCALAPPDATA": os.getenv("LOCALAPPDATA"),
    "TEMP": os.getenv("TEMP"),
    "SYSTEMROOT": os.getenv("SystemRoot"),

}

agent_workflow = AgentWorkflow(
    agents=[agent_orchestrator, file_agent, powershell_agent],
    root_agent="AgentOrchestrator",
    initial_state={
        'system_variables': info,
    }
)

