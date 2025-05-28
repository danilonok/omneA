from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context
from tavily import AsyncTavilyClient
import os

async def search_web(query: str) -> str:
    """Useful for using the web to answer questions. Provide concise query."""
    client = AsyncTavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
    return str(await client.search(query))


web_search_agent = FunctionAgent(
    name='WebSearchAgent',
    description='Useful for searching any information in Web. Use it whenever you need.',
    system_prompt=(
        "You are WebSearchAgent that can perform search of information in WEB."
        "Given a request, you should fulfil it and provide concise response as a report of your work."
        "After you have completed your actions, handoff to AgentOrchestrator!"
        "Always return back to AgentOrchestrator. Be sure you finish with a handoff."

    ),
    tools=[search_web],
    can_handoff_to=['AgentOrchestrator']
)