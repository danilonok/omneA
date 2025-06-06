
from llama_index.core.agent.workflow import AgentWorkflow
from configs.llm_config import Settings
from workflows.file_agent import file_agent
from workflows.powershell_agent import powershell_agent
from workflows.agent_orchestrator import agent_orchestrator
from workflows.run_app_agent import run_app_agent
from workflows.web_search_agent import web_search_agent
from workflows.media_control_agent import media_control_agent

from datetime import datetime
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
    'System date': datetime.now().date(),
    'System time of workflow execution': datetime.now().time()

}

agent_workflow = AgentWorkflow(
    agents=[agent_orchestrator, file_agent, powershell_agent, run_app_agent, web_search_agent, media_control_agent],
    root_agent="AgentOrchestrator",
    initial_state={
        'system_variables': info,
    }
)

