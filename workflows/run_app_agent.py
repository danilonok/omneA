from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context

import pandas as pd
import subprocess

df = pd.read_csv("InstalledApps.csv")


def get_app_path(app_name):
    row = df[df['Name'] == app_name]
    if not row.empty:
        return row.iloc[0]['Path']

    partial = df[df['Name'].str.contains(app_name, case=False, na=False)]
    if not partial.empty:
        return partial.iloc[0]['Path']
    return None

async def run_app(ctx: Context, app_name: str):
    """Useful for running applications in Windows 11 PC. Your input should contain a name of an app."""

    app_path = get_app_path(app_name)
    if app_path:
        subprocess.Popen([app_path])
    else:
        return f"App {app_name} not found."
    return f'App {app_name} was successfully launched.'


run_app_agent = FunctionAgent(
    name='RunAppAgent',
    description='Useful for running installed apps in Windows. Handoff to me first! Do not call my functions!',
    system_prompt=(
        "You are RunAppAgent that can run different installed apps in Windows."
        "Given a request, you should fulfil it and provide concise response as a report of your work."
        "After you have completed your actions, handoff to AgentOrchestrator!"
        "Always return back to AgentOrchestrator. Be sure you finish with a handoff."
    ),
    tools=[run_app],
    can_handoff_to=['AgentOrchestrator']
)