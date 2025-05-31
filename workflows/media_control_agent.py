import keyboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from llama_index.core.agent.workflow import FunctionAgent

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))



async def play() -> str:
    """Useful for sending start playback signal to system."""
    keyboard.send("play/pause media")
    return 'System received play command.'

async def pause() -> str:
    """Useful for sending playback pause signal to system."""
    keyboard.send("play/pause media")
    return 'System received pause command.'

async def next_track() -> str:
    """Useful for sending next track signal to system."""
    keyboard.send("next track")
    return 'System received next track command.'

async def previous_track() -> str:
    """Useful for sending previous track signal to system."""
    keyboard.send("previous track")
    return 'System received previous track command.'
async def set_volume_level(volume_level: int) -> str:
    """Useful for setting system volume level. Your input must contain int value of volume level from 0 to 100."""
    volume.SetMasterVolumeLevelScalar(volume_level/100, None)
    return f'Volume level set to {volume_level}.'
async def get_volume_level() -> str:
    """Useful for getting system volume level."""
    current = volume.GetMasterVolumeLevelScalar()
    return f"Current Volume: {current*100}%."

media_control_agent = FunctionAgent(
    name='MediaControlAgent',
    description='Useful for controlling media in Windows. Can switch tracks, pause and unpause them and set and get system volume level.',
    system_prompt=(
        "You are MediaControlAgent that can control media in Windows 11."
        "Given a request, you should fulfil it and provide concise response as a report of your work."
        "If the system asks you to do a task, which requires additional information, do NOT make it up! For example, if you need to check some system parameters, handoff to AgentOrchestrator for extra info."
        "After you have completed your actions, handoff to AgentOrchestrator!"
        "Always return back to AgentOrchestrator. Be sure you finish with a handoff."
    ),
    tools=[play, pause, next_track, previous_track, set_volume_level, get_volume_level],
    can_handoff_to=['AgentOrchestrator']
)

