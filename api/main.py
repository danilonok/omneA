
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult,
    AgentStream,
)
from llama_index.core.prompts import PromptTemplate

from core.logging.agent_logger import AgentLogger, LogType
from core.history.history_manager import HistoryManager
from workflows.agent_orchestrator import agent_orchestrator, examples
from workflows.agent_workflow import agent_workflow
from llama_index.core.workflow import Context
import json
from fastapi.encoders import jsonable_encoder
from core.few_shot_prompt_enrichment.create_nodes import retriever

import os
from dotenv import load_dotenv

import time
import math
# import logger_phoenix


load_dotenv()
agent_logger = AgentLogger('C:/Agents/Logs/log.txt')
history_manager = HistoryManager('C:/Agents/History/history.json')
agent_logger.readLogFile()
history_manager.readHistoryFile()
app = FastAPI()


def update_prompt(query: str):
    nodes = retriever.retrieve(query)

    examples = ""
    for node in nodes:
        examples += f'Query: {node.text}\nSteps:{node.metadata["steps"]}\n'

    # Format the entire prompt string with examples
    ex = '{{"input": "hello world", "num_beams": 5}}'
    ex_bad = '{{\'input\': \'hello world\', \'num_beams\': 5}}'
    prompt_text = f"""
        You are an orchestrator agent of OmniA - multi-agent system, designed to assist user in performing different action in Windows 11 operating system.
        You are main controlling agent of the whole agentic system. 

        ## Tools

        You have access to a single tool, that can delegate performing an action to another functional agents. You are responsible for using the tools in any sequence you deem appropriate to complete the task at hand.
        This may require breaking the task into subtasks and using different tools to complete each subtask.
        You are able to perform only Handoff operation and nothing else. Any tries to perform extra action will result in complete system failure.


        You have access to the following tool:
        {{tool_desc}}


        ## Output Format

        Please answer in the same language as the question and use the following format:

        ```
        Thought: The current language of the user is: (user's language). I need to use a tool to help me answer the question.
        Action: tool name (one of {{tool_names}}) if using a tool.
        Action Input: the input to the tool, in a JSON format representing the kwargs (e.g. {ex})
        ```

        Please ALWAYS start with a Thought.

        NEVER surround your response with markdown code markers. You may use code markers within your response if you need to.

        Please use a valid JSON format for the Action Input. Do NOT do this {ex_bad}.

        If this format is used, the tool will respond in the following format:

        ```
        Observation: tool response
        ```

        You should keep repeating the above format till you have enough information to answer the question without using any more tools. At that point, you MUST respond in one of the following two formats:

        ```
        Thought: I can answer without using any more tools. I'll use the user's language to answer
        Answer: [your answer here (In the same language as the user's question)]
        ```

        ```
        Thought: I cannot answer the question with the provided tools.
        Answer: [your answer here (In the same language as the user's question)]
        ```

        Rules:
        1) Never handoff to yourself. It crushes the system.
        2) Give concise but accurate handoff reasons.
        3) Never tell the user in final answer that operation is being executed by something. If you were not able to execute the user's query, be polite and ask him to rerun the workflow.
        4) There are some request that doesn't require any handoff, like "Who are you?" or "Hello, how are you?". In this case, you should answer the question directly.
        5) Before telling user about the unsuccess in fulfilling the request, try to make PowershellAgent do the request. It is very capable.

        Here are the examples of frequent requests and how to orchestrate the agentic system:
        {examples}

        ## Current Conversation

        Below is the current context, that contains user messages and agent responses.

        """

    # Create a new prompt template with the examples already filled in
    prompt = PromptTemplate(prompt_text)

    # Update the agent with the formatted prompt
    agent_workflow.agents['AgentOrchestrator'].update_prompts({"react_header": prompt})

@app.get("/hi")
def read_root():
    return {"Hello": "World"}

@app.get("/history")
def get_history():
    entries = jsonable_encoder(history_manager.history_entries)
    return entries

@app.get("/logs")
def get_logs():
    entries = jsonable_encoder(agent_logger.get_last_logs(50))
    return entries

@app.post("/logs/delete")
def delete_logs():
    print('Logs deleted')
    agent_logger.delete_logs()

@app.post("/history/delete")
def delete_history():
    print('History cleared')

    history_manager.delete_history()

@app.websocket("/ws/agent")
async def websocket_agent(websocket: WebSocket):
    await websocket.accept()
    try:
        ctx = Context(agent_workflow)

        while True:
            try:
                query = await websocket.receive_text()
                update_prompt(query)
                history_manager.add_history_entry(title=str(query).strip())
                history_manager.saveHistoryFile()
                start_time = time.time()
                handler = agent_workflow.run(
                    user_msg=(str(query)), ctx=ctx
                )
                agent_logger.log('AgentWorkflow', LogType.input_message, str(query))
                current_agent = None
                current_tool_calls = ""
                async for event in handler.stream_events():
                    if (
                            hasattr(event, "current_agent_name")
                            and event.current_agent_name != current_agent
                    ):
                        current_agent = event.current_agent_name
                        agent_logger.log(str(current_agent), LogType.current_agent, f'Agent: {current_agent}')

                        print(f"\n{'=' * 50}")
                        print(f"🤖 Agent: {current_agent}")
                        print(f"{'=' * 50}\n")

                    elif isinstance(event, AgentOutput):
                        if event.response.content:
                            print("📤 Output:", event.response.content)
                            agent_logger.log(str(current_agent), LogType.agent_output, f'Output: {event.response.content}')
                        if event.tool_calls:
                            print(
                                "🛠️  Planning to use tools:",
                                [call.tool_name for call in event.tool_calls],
                            )
                    elif isinstance(event, ToolCallResult):
                        print(f"🔧 Tool Result ({event.tool_name}):")
                        print(f"  Arguments: {event.tool_kwargs}")
                        print(f"  Output: {event.tool_output}")
                        agent_logger.log(str(current_agent), LogType.tool_result, f'Tool Result ({event.tool_name}):\nArguments: {event.tool_kwargs}\nOutput: {event.tool_output}')

                    elif isinstance(event, ToolCall):
                        if str(event.tool_name) == 'handoff':
                            await websocket.send_text(json.dumps({
                                'type': 'step',
                                'content': f'Calling agent: {str(event.tool_kwargs['to_agent'])}',
                                'reason': f'Reason: {str(event.tool_kwargs['reason'])}'
                            }))
                        print(f"🔨 Calling Tool: {event.tool_name}")
                        print(f"  With arguments: {event.tool_kwargs}")

                        agent_logger.log(str(current_agent), LogType.tool_call, f'Calling Tool: {event.tool_name}:\n With arguments: {event.tool_kwargs}')
                response = await handler
                agent_logger.saveLogFile()
                end_time = time.time()
                time_delta = end_time - start_time
                print('Request executed in: ',time_delta)
                await websocket.send_text(json.dumps({
                    'type': 'report',
                    'content': str(response),
                    'time': math.trunc(time_delta * 100) / 100.
                }))
            except WebSocketDisconnect:
                print("Client disconnected")
                break
            except Exception as e:
                print(f"Error processing query: {e}")
                await websocket.send_text(json.dumps({
                    'type': 'error',
                    'content': str(e)
                }))
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()


