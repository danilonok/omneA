from alembic.command import history
from fastapi import FastAPI, WebSocket
from llama_index.core.agent.workflow import (
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult,
    AgentStream,
)
from core.logging.agent_logger import AgentLogger, LogType
from core.history.history_manager import HistoryManager
from workflows.agent_workflow import agent_workflow
from llama_index.core.workflow import Context
import json
from fastapi.encoders import jsonable_encoder

import os
from dotenv import load_dotenv

import time
import math

load_dotenv()
agent_logger = AgentLogger('C:/Agents/Logs/log.txt')
history_manager = HistoryManager('C:/Agents/History/history.json')
agent_logger.readLogFile()
history_manager.readHistoryFile()
app = FastAPI()


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

    ctx = Context(agent_workflow)

    while True:
        query = await websocket.receive_text()
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

            # if isinstance(event, AgentStream):
            #     if event.delta:
            #         print(event.delta, end="", flush=True)
            # elif isinstance(event, AgentInput):
            #     print("📥 Input:", event.input)



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

        response = await handler # or step.json() if structured
        agent_logger.saveLogFile()
        end_time = time.time()
        time_delta = end_time - start_time
        print('Request executed in: ',time_delta)
        await websocket.send_text(json.dumps({
            'type': 'report',
            'content': str(response),
            'time': math.trunc(time_delta * 100) / 100.
        }))




    #await websocket.close()

