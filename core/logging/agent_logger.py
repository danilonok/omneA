from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum

import json

class LogType(str, Enum):
    input_message = 'input_message'
    current_agent = 'current_agent'
    tool_call = 'tool_call'
    tool_result = 'tool_result'
    agent_output = 'agent_output'

class Log(BaseModel):
    agent: str
    type: LogType
    log_text: str
    timestamp: datetime = Field(default_factory=datetime.now)
    id: UUID = Field(default_factory=uuid4)

class AgentLogger:
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.logs = []

    def saveLogFile(self):
        with open(self.log_file, "w") as f:
            json.dump([log.dict() for log in self.logs], f, indent=4, default=str)
    def readLogFile(self):
        try:
            with open(self.log_file, "r") as f:
                logs_data = json.load(f)
            self.logs = [Log.model_validate(item) for item in logs_data]
        except FileNotFoundError:
            with open(self.log_file, "w") as f:
                f.write('')
            self.logs = []
        except json.decoder.JSONDecodeError:
            with open(self.log_file, "w") as f:
                f.write('')
            self.logs = []

    def log(self, agent_name: str, type: LogType, log_content: str):
        log = Log(agent=agent_name, type=type, log_text=log_content)
        self.logs.append(log)

    def get_last_logs(self, n: int = 50):
        return self.logs[-n:]

    def delete_logs(self):
        self.logs = []
        with open(self.log_file, "w") as f:
            f.write('')


