from few_shot_generation.generate_tasks import TaskGenerator
from few_shot_generation.generate_commands import CommandGenerator
from few_shot_generation.generate_env_setup import EnvSetupGenerator
from few_shot_generation.create_dataset import Dataset
import json
# generator = TaskGenerator()

# response = generator.generate(15)



# # print(response)
# # tasks = []
# # for task in response:
# #     tasks.append(task.task)

# # with open('tasks.json', 'w') as f:
# #     json.dump(tasks, f)

# commands = {}
# for task in response:
#     print('Generating commands for: ' + task.task)
#     command_generator = CommandGenerator()
#     commands[task.task] = command_generator.generate(task.task)
# print(commands)


# # test_task = 'Rename all the .txt files in the D:\Work folder to include the current date.'
# # commands = {}
# # command_generator = CommandGenerator()
# # commands[test_task]= command_generator.generate(test_task)

# # print(commands)
# dataset = Dataset(commands=commands)
# dataset.create_dataset()

# dataset.save_dataset('dataset.json')


env_creator = EnvSetupGenerator()

response = env_creator.generate('Rename all files with .txt extension to .log in My Files directory.', ["Get-ChildItem -Path 'My Files' -Filter '*.txt'",
            "%{$_.Name.Substring(0,$_.Name.Length-4)} | Get-Unique",
            "Foreach-Object {Rename-Item -Path (Join-Path -Path 'My Files' -ChildPath ($_.ToString() + '.txt')) -NewName ('{0}.log' -f $_.ToString())}"])
print(response)