from tools.tool import Tool
import shutil
import re
"""
File system tool allows the agent-system to perform various tasks with Windows File System, such as:
Copying/Moving files, deleting files, reading files (text files in most popular formats), edit text files.
"""

class FileSystemTool(Tool):
    """
    File system tool allows the agent-system to perform various tasks with Windows File System, such as:
    Copying/Moving files, deleting files, reading files (text files in most popular formats), edit text files.
    """
    syntax = f"""
Copying: FS_TOOL(copy, filepath, path_to)
Moving: FS_TOOL(move, filepath path_to)
Deleting: FS_TOOL(delete, filepath)
Read: FS_TOOL(read, filepath)
Editing: FS_TOOL(edit, new_content)
"""
    def __init__(self):
        super().__init__()
    def execute(self, command: str):
        match = re.search(r"```(?:\w+\n)?(.*?)```", command, re.DOTALL)

    def copy_file(source_path: str, destination_path: str):
        """
        Copy a file from source_path to destination_path

        :param source_path: Path to the source file
        :param destination_path: Path to the destination file
        """
        try:
            shutil.copy2(source_path, destination_path)
            print(f"File copied from {source_path} to {destination_path}")
        except FileNotFoundError:
            print(f"File not found: {source_path}")
        except PermissionError:
            print(f"Permission denied: {destination_path}")

