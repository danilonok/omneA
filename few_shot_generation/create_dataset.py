from few_shot_generation.generate_commands import Command
from typing import List, Dict
from collections import defaultdict
import json
import os
class Dataset:
    def __init__(self, commands: Dict[str, List[Command]]):
        self.commands = commands
        self.dataset = []
    def create_dataset(self):
        for task, commands in self.commands.items():
            d = []
            for command in commands:
                d.append(command.command)
            self.dataset.append({
                'query': task,
                'commands': d
            })
    def save_dataset(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.dataset, f)