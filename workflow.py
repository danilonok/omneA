from steps import steps_parser, Steps
from commands import commands_parser
from tools.command_executor import execute_cmd_command
from llama_index.core import PromptTemplate
from llama_index.core.workflow import draw_all_possible_flows

from pydantic_core import ValidationError

query_str = 'Find file day_report.txt in my C:/Work folder and summarize it'


from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
    Context
)
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register
from configs.llm_config import llm


tracer_provider = register(
  project_name="my-llm-app", # Default is 'default'
  endpoint="http://localhost:6006/v1/traces",
)
LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

class StepsProduced(Event):
    steps: Steps

class StartEventWrapper(Event):
    query: str

class BadCommand(Event):
    error: str

class CommandGenerated(Event):
    step_results : str

class LastStepExecuted(Event):
    result: str
RESPONSE_PROMPT_TMP = (
    "You are the last agent in PC Assistant Workflow. You provide user with brief responses about their request. No technical details!"
    "You are given the output of the execution of the last step to fulfill user request."
    "The output:"
    "{output}"
    "Query:"
    "{query}"
    "The whole workflow consists of such steps:"
    "{steps}"
    "Give a user information about his request using provided information. If the last step was to get some information, just give it to the user."
)

RESPONSE_PROMPT = PromptTemplate(RESPONSE_PROMPT_TMP)
class BasicWorkflow(Workflow):
    @step
    async def start_event_wrapper(self, ctx: Context, ev: StartEvent) -> StartEventWrapper:
        return StartEventWrapper(query=ev.query)
    @step
    async def produce_steps(self, ctx: Context, ev: StartEventWrapper) -> StepsProduced:
        await ctx.set('query', ev.query)
        await ctx.set('unsuccessful_attempts', 0)

        try:
            response = steps_parser(query=ev.query)
            print(response)
            await ctx.set('steps', response.steps)
            await ctx.set('current_step', response.steps[0])
            await ctx.set('step_count', len(response.steps))
            return StepsProduced(steps=response)
        except ValidationError as e:
            print("Validation Error:", e)



    @step
    async def generateCommand(self, ctx: Context, ev: StepsProduced | CommandGenerated | BadCommand) -> CommandGenerated | BadCommand | LastStepExecuted:

        if await ctx.get('unsuccessful_attempts') > 5:
            return StartEventWrapper(query=await ctx.get('query'))

        # execute the first step of plan
        if isinstance(ev, StepsProduced):
            current_step = await ctx.get('current_step')
            commands = []

            while len(commands) == 0:
                try:
                    commands = commands_parser(query=await ctx.get('query'), step=current_step.text,
                                           prev_step_output='There were no steps before this.').commands
                except:
                    print('Error parsing commands')
            step_results = []
            for command in commands:
                result = execute_cmd_command(command.text)
                if result == 'Command output: ':
                    result = 'Command execution provided no additional info.'
                if 'Command error:' in result:
                    await ctx.set('unsuccessful_attempts', await ctx.get('unsuccessful_attempts') + 1)
                    return BadCommand(error=f'Command {command} executed with error: {result}')
                step_results.append({'command': command, 'result': result})
            await ctx.set('previous_step', current_step)

            if await ctx.get('step_count') > 1:
                steps = await ctx.get('steps')
                current_index = steps.index(current_step)
                await ctx.set('current_step', steps[current_index + 1])
                return CommandGenerated(step_results = str(step_results))
            else:
                return LastStepExecuted(result=str(step_results))
        if isinstance(ev, BadCommand):
            current_step = await ctx.get('current_step')
            commands = []
            while len(commands) == 0:
                try:
                    commands = commands_parser(query=await ctx.get('query'), step=current_step.text,
                                               prev_step_output= ev.error).commands
                except:
                    print('Error parsing commands')
            step_results = []
            for command in commands:
                result = execute_cmd_command(command.text)
                if result == 'Command output: ':
                    result = 'Command execution provided no additional info.'
                if 'Command error:' in result:
                    await ctx.set('unsuccessful_attempts', await ctx.get('unsuccessful_attempts') + 1)
                    return BadCommand(error=f'Command {command} executed with error: {result}')
                step_results.append({'command': command, 'result': result})


            await ctx.set('previous_step', step_results)
            steps = await ctx.get('steps')  # Await to get the actual list
            current_step = await ctx.get('current_step')  # Await current step
            step_count = await ctx.get('step_count')  # Await step count

            if steps.index(current_step) + 1 < step_count:
                current_index = steps.index(current_step)  # Find the index
                await ctx.set('current_step', steps[current_index + 1])  # Set the next step

                return CommandGenerated(step_results = str(step_results))
            return LastStepExecuted(result=str(step_results))
        if isinstance(ev, CommandGenerated):
            current_step = await ctx.get('current_step')
            commands = []

            while len(commands) == 0:
                try:
                    commands = commands_parser(query=await ctx.get('query'), step=current_step.text,
                                           prev_step_output= str(await ctx.get('previous_step', default=None)) or 'There were no steps before this.').commands
                except:
                    print('Error parsing commands')
            step_results = []
            for command in commands:
                result = execute_cmd_command(command.text)
                if result == 'Command output: ':
                    result = 'Command execution provided no additional info.'
                if 'Command error:' in result:
                    await ctx.set('unsuccessful_attempts', await ctx.get('unsuccessful_attempts') + 1)
                    return BadCommand(error=f'Command {command} executed with error: {result}')
                step_results.append({'command': command, 'result': result})

            await ctx.set('previous_step', step_results)
            steps = await ctx.get('steps')  # Await to get the actual list
            current_step = await ctx.get('current_step')  # Await current step
            step_count = await ctx.get('step_count')  # Await step count

            if steps.index(current_step) + 1 < step_count:

                current_index = steps.index(current_step)  # Find the index
                await ctx.set('current_step', steps[current_index + 1])  # Set the next step
                return CommandGenerated(step_results = str(step_results))
            return LastStepExecuted(result=str(step_results))
    @step
    async def synthesize_response(self, ctx: Context, ev: LastStepExecuted) -> StopEvent:
        prompt = RESPONSE_PROMPT.format(query=await ctx.get('query'), steps=str(await ctx.get('steps')), output=ev.result)
        response = await llm.acomplete(prompt)
        return StopEvent(result=str(response))

    def restart_workflow(self):
        # Logic to restart the workflow
        # This could involve resetting state, logging, and re-emitting the StartEvent
        self.reset_state()
        self.emit_event(StartEvent())

async def main():
    w = BasicWorkflow(timeout=40, verbose=True)
    draw_all_possible_flows(w, "workflow.html")
    result = await w.run(query=query_str)


    print(result)
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# steps_list = steps_parser(query=query_str)
# print(steps_list)
#
# # we got list of steps
#
# # generate a command for step 1
# commands = commands_parser(query=query_str, step=steps_list.steps[0].text, prev_step_output='There were no steps before this.')
#
# print(commands)
#
# # execute commands
# step_results = []
# for command in commands.commands:
#     result = execute_cmd_command(command.text)
#     if result == 'Command output: ':
#         result = 'Command execution provided no additional info.'
#     step_results.append({'command' : command, 'result' : result})
#
# print(step_results)
#
# # generate a command for step 2
# commands = commands_parser(query=query_str, step=steps_list.steps[1].text, prev_step_output=step_results)
#
# print(commands)
#
# # execute commands
# step_results = []
# for command in commands.commands:
#     result = execute_cmd_command(command.text)
#     if result == 'Command output: ':
#         result = 'Command execution provided no additional info.'
#     step_results.append({'command' : command, 'result' : result})
#
# print(step_results)
#
#
# # generate a command for step 3
# commands = commands_parser(query=query_str, step=steps_list.steps[2].text, prev_step_output=step_results)
#
# print(commands)
#
# # execute commands
# step_results = []
# for command in commands.commands:
#     result = execute_cmd_command(command.text)
#     if result == 'Command output: ':
#         result = 'Command execution provided no additional info.'
#     step_results.append({'command' : command, 'result' : result})
#
# print(step_results)