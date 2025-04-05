from few_shot_generation.generate_tasks import TaskGenerator
from few_shot_generation.generate_commands import CommandGenerator
from few_shot_generation.create_dataset import Dataset
generator = TaskGenerator()

response = generator.generate(2)

print(response)

commands = {}
for task in response:
    print('Generating commands for: ' + task.task)
    command_generator = CommandGenerator()
    commands[task.task] = command_generator.generate(task.task)
print(commands)

dataset = Dataset(commands=commands)
dataset.create_dataset()

dataset.save_dataset('dataset.json')