from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context

import os


import shutil
import os
import send2trash
import glob

async def copy_file(ctx: Context, origin: str, destination: str) -> str:
    """Useful for copying file from origin location in PC to destination location. Your input must contain full paths of origin and destination of a copy operation. Both must contain name of file with an extension at the end
    Example: origin: C:/file.txt, destination: D:/file.txt
    """
    # Copy file from origin to destination
    try:
        shutil.copy2(origin, destination)
        return f'File from {origin} copied to {destination} successfully.'
    except FileNotFoundError:
        return "Source file not found."
    except PermissionError:
        return "Permission denied."
    except Exception as e:
        return f"An error occurred: {e}"



async def create_file(ctx: Context, file_path:str) -> str:
    """Useful for creating an empty file using the path. Your input must contain and full path of a future file containing name of a file with extension. For example, 'C:/Work/test.txt'
    Be sure you've included the full path with file name! """
    # Create file
    try:
        with open(file_path, 'x') as file:
            pass
        return f'File was created in {file_path} successfully.'
    except FileExistsError:
        return "File already exists."
    except Exception as e:
        return f"An error occurred: {e}"


async def delete_file(ctx: Context, file_path:str) -> str:
    """Useful for deleting a file using the path. Your input must contain a full path of a file."""
    # Delete file
    try:
        send2trash.send2trash(file_path.replace('/', '\\'))
        return f'File {file_path} was deleted successfully.'
    except FileNotFoundError:
        return "File not found."
    except PermissionError:
        return "Permission denied."
    except Exception as e:
        return f"An error occurred: {e}"


async def write_file(ctx: Context, content: str, file_path:str) -> str:
    """Useful for writing to an existing file. Your input must contain a full path of a file and a content as a string."""
    # Write to file
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return f'Content was written successfully to {file_path}'
    except PermissionError:
        return "Permission denied."
    except Exception as e:
        return f"An error occurred: {e}"


async def read_file(ctx: Context, file_path:str) -> str:
    """Useful for reading content of a file using its path. Your input must contain a full path of a file."""
    # Read file
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return f'Contents: \n{content}'
    except FileNotFoundError:
        return "File not found."
    except PermissionError:
        return "Permission denied."


async def dir_path(ctx: Context, path:str) -> str:
    """Useful for checking structure of a file system given path. Your input must contain a path."""
    # Dir folders
    def print_tree(startpath, max_depth=3, indent="  "):
        content = ''
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            if level >= max_depth:
                continue
            indent_str = indent * level
            content += f"{indent_str}{os.path.basename(root)}/\n"
            subindent = indent * (level + 1)
            for f in files:
                content += f"{subindent}{f}\n"
        return content
    return f'Structure of a path {path}:\n{print_tree(path)}'

async def search(ctx: Context, full_pattern: str, recursive=False) -> str:
    """Useful for searching for files using python glob module. Your input must contain full pattern for search with glob.glob.
    If recursive search is requested, use the `**/` wildcard and set `recursive=True`
    Pattern should contain the file name pattern (e.g., `*.txt`, `data-??.csv`, `**/*.py`). It should also contain path where to look for file, like this: C:/Games/**/*.txt.
    Use recursive field whether to search subdirectories (`true` or `false`)"""

    files = glob.glob(full_pattern, recursive=recursive)
    return f'Search results: {sorted(files)}' if files else "No matching files found."

async def rename(ctx: Context, old_path: str, new_path: str) -> str:
    """Useful for renaming a file. Your input must contain a full original path and a full new renamed path.
    Example: old_path: C:/file.txt, new_path: C:/new_file.txt
    """
    try:
        os.rename(old_path, new_path)
        return f'File renamed from {old_path} to {new_path} successfully.'
    except FileNotFoundError:
        return "Source file not found."
    except FileExistsError:
        return "Destination file already exists."
    except PermissionError:
        return "Permission denied."
    except IsADirectoryError:
        return "A directory was specified where a file was expected."
    except NotADirectoryError:
        return "A component of the path is not a directory."
    except OSError as e:
        return f"OS error occurred: {e}"


file_agent = FunctionAgent(
    name='FileAgent',
    description='Useful for operating with PC\'s file system. Use it for any file operations like creating and writing files, reading files, moving them etc.',
    system_prompt=(
        "You are FileAgent that can perform various actions with PC's file system."
        "Given a request, you should fulfil it and provide concise response as a report of your work."
        "If the system asks you to do a task, which requires additional information, do NOT make it up! For example, if you need to check some system parameters, handoff to AgentOrchestrator for extra info."
        "After you have completed your actions, handoff to AgentOrchestrator!"
        "Always return back to AgentOrchestrator. Be sure you finish with a handoff."
    ),
    tools=[copy_file, create_file, write_file, delete_file, read_file, dir_path, search, rename],
    can_handoff_to=['AgentOrchestrator']
)

