import subprocess
import shlex
import os
DANGEROUS_COMMANDS = [
    "Remove-Item", "Format-Volume", "Clear-Content", "Stop-Process",
    "Stop-Computer", "Restart-Computer", "Set-ExecutionPolicy",
    "net user", "net localgroup", "Enable-PSRemoting",
    "New-SmbShare", "Invoke-WebRequest", "Test-Connection",
    "New-Object System.Net.Sockets.TcpClient", "Set-ItemProperty",
    "Remove-Item -Path", "IEX (New-Object Net.WebClient)",
    "Get-Process lsass", "Remove-Partition", "Format-Volume", "Set-Volume"
]
current_dir = None

def execute_cmd_command(command: str) -> str:
    """Execute Windows Powershell command on local machine. Returns stdout and stderr of executed command. If strings are empty, command is executed."""
    # commands = shlex.split(command)
    # if 'powershell' not in commands and '-Command' not in commands:
    #     commands.insert(0, 'powershell')
    #     commands.insert(1, '-Command')



    # global current_dir
    #

    #     if current_dir:
    #         os.chdir(current_dir)
    #     print(f'Sys message: executed command {commands}')
    #     if 'cd' in commands:
    #         current_dir = commands[1]
    try:
        if not is_safe_command(command):
            return f'Command output: This PowerShell command is blocked for security reasons!'

        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, shell=True,stdin=subprocess.DEVNULL)
        if result.returncode != 0:
            return f'Command error: {result.stderr}'
        elif result.stdout.strip() != '':
            return f'Command output: {result.stdout}'
        else:
            return "Command output: There is no output. Hint: It usually means the command executed successfully"

    except Exception as e:
        return str(e)

def is_safe_command(command: str) -> bool:
    """Check if the command contains dangerous PowerShell keywords."""
    command_lower = command.lower()
    return not any(dangerous.lower() in command_lower for dangerous in DANGEROUS_COMMANDS)
