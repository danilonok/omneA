from pydantic import BaseModel, Field

class Settings(BaseModel):
    language: str


class SettingsManager:
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.settings = None


