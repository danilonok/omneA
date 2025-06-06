from openai import OpenAI
from pydantic import BaseModel
from typing import List
import os

client = OpenAI(api_key=os.getenv('openai_api'))

input = """
You must generate pairs query - steps, that are required to perform a task as if you were an PC-Assistant multiagent-system that fulfils user requests.
You are an orchestrating agent, that delegates tasks to another functional agents.

Available agents:
**FileAgent** – Useful for operating with PC's file system. Handles file creation, reading, writing, copying, deletion, directory inspection, renaming, and file search.

**Tools:**

- `copy_file(origin: str, destination: str)` – Copies a file from origin to destination. Full file paths required.
    
- `create_file(file_path: str)` – Creates an empty file at the specified path. Requires full path including filename and extension.
    
- `write_file(content: str, file_path: str)` – Writes string content to a file at the specified path.
    
- `delete_file(file_path: str)` – Deletes a file at the specified full path.
    
- `read_file(file_path: str)` – Reads and returns the content of a file.
    
- `dir_path(path: str)` – Returns a tree view of the directory structure up to 3 levels deep for the given path.
    
- `search(full_pattern: str, recursive: bool)` – Searches for files using glob pattern matching. Supports recursive search.
    
- `rename(old_path: str, new_path: str)` – Renames or moves a file from old_path to new_path.


**MediaControlAgent** – Useful for controlling media playback and system volume in Windows. Can play/pause media, switch tracks, and set or get the system volume level.

**Tools:**

- `play()` – Sends a system-level command to start/resume media playback.
    
- `pause()` – Sends a system-level command to pause media playback.
    
- `next_track()` – Skips to the next media track.
    
- `previous_track()` – Goes back to the previous media track.
    
- `set_volume_level(volume_level: int)` – Sets system volume to a specified level (0–100).
    
- `get_volume_level()` – Retrieves and reports the current system volume level.


**PowershellAgent** – Useful for creating and executing various PowerShell commands in Windows 11. Can handle tasks like API calls, opening websites, and more. Very powerful for system-level automation.

**Tools:**

- `generate_command(query: str)` – Uses an LLM-based system to generate one or more PowerShell commands based on the provided natural language query.
    
- `execute_command(command: str)` – Executes a single, properly formatted PowerShell command on the system.

**RunAppAgent** – Useful for launching installed applications in Windows (e.g., browsers, editors, games). **Cannot run scripts directly.**

**Tools:**

- `run_app(app_name: str)` – Launches an installed application by its name. Matches exact or partial name from a predefined CSV of installed apps. Returns an error if not found.

**WebSearchAgent** – Useful for searching any information on the web. Use it whenever external up-to-date knowledge is required.

**Tools:**

- `search_web(query: str)` – Performs a web search using the Tavily API with a concise query. Returns search results as a string.


Example:
Query: Open the URL https://example.com in the default browser
Steps:
1) PowershellAgent -> generate_command('Open https://example.com in browser')
2) PowershellAgent -> execute_command('<generated command>')

You must create 30 pairs. Create such queries that require at least three agentic calls. 

"""


class QueryStepsPair(BaseModel):
    query: str
    steps: List[str]

class QueryStepsPairs(BaseModel):
    pairs: List[QueryStepsPair]

response = client.responses.parse(
    model="gpt-4o",
    input=input,
    text_format=QueryStepsPairs

)

print(response.output_parsed)
import json

with open('steps2.json', 'w') as data:
    data.write(response.output_parsed.model_dump_json())