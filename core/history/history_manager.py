import json
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

class HistoryEntry(BaseModel):
    title: str
    timestamp: datetime = Field(default_factory=datetime.now)
    id: UUID = Field(default_factory=uuid4)

class HistoryManager:
    def __init__(self, history_file):
        self.history_file = history_file
        self.history_entries = []

    def saveHistoryFile(self):
        with open(self.history_file, "w") as f:
            json.dump([history.dict() for history in self.history_entries], f, indent=4, default=str)

    def readHistoryFile(self):
        try:
            with open(self.history_file, "r") as f:
                history_data = json.load(f)
            self.history_entries = [HistoryEntry.model_validate(item) for item in history_data]
        except FileNotFoundError:
            with open(self.history_file, "w") as f:
                f.write('')
            self.history_entries = []
        except json.decoder.JSONDecodeError:
            with open(self.history_file, "w") as f:
                f.write('')
            self.history_entries = []

    def add_history_entry(self, title: str):
        history = HistoryEntry(title=title)
        self.history_entries.append(history)

