from few_shot_generation.generate_tasks import TaskGenerator

generator = TaskGenerator()

response = generator.generate(5)
print(response)