from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context
from multipart import file_path


async def copy_file(ctx: Context, origin: str, destination: str) -> str:
    """Useful for copying file from origin location in PC to destination location. Your input must contain full paths of origin and destination of a copy operation"""
    # Copy file from origin to destination
    raise NotImplementedError()
    return f'File from {origin} copied to {destination} successfully.'

async def create_file(ctx: Context, name: str, file_path:str) -> str:
    """Useful for creating a file using the path. Your input must contain name of a file with extension and full path of a place, where this file should be created."""
    # Create file
    raise NotImplementedError()
    return f'File {name} was created in {file_path} successfully.'

async def delete_file(ctx: Context, file_path:str) -> str:
    """Useful for deleting a file using the path. Your input must contain a full path of a file."""
    # Delete file
    raise NotImplementedError()
    return f'File {file_path} was deleted successfully.'

async def write_file(ctx: Context, content: str, file_path:str) -> str:
    """Useful for writing to an existing file. Your input must contain a full path of a file and a content as a string."""
    # Write to file
    raise NotImplementedError()
    return f'Content {content[:50]} was written successfully to{file_path}'


file_agent = FunctionAgent(
    name='FileAgent',
    description='Useful for operating with PC\'s file system. Use it for any file operations.',
    system_prompt=(
        "You are FileAgent that can perform various actions with PC's file system."
        "Given a request, you should fulfil it and provide concise response as a report of your work."
    ),
    tools=[copy_file],
    can_handoff_to=['AgentOrchestrator']
)

