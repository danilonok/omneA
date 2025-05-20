from fastapi import FastAPI, WebSocket
from typing import Union
from reactAgent_test import agent_2
from llama_index.core.agent.workflow import AgentStream, ToolCallResult
from llama_index.core.workflow import Context


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.websocket("/ws/agent")
async def websocket_agent(websocket: WebSocket):
    await websocket.accept()
    ctx = Context(agent_2)

    while True:
        query = await websocket.receive_text()
        handler = agent_2.run(query, ctx=ctx)
        async for ev in handler.stream_events():
            if isinstance(ev, ToolCallResult):
                await websocket.send_text(f"\nCall {ev.tool_name} with {ev.tool_kwargs}\nReturned: {ev.tool_output}")
            # if isinstance(ev, AgentStream):
            #     await websocket.send_text(f"{ev.delta}")


        #result = agent_2.chat(query)
        response = await handler # or step.json() if structured
        await websocket.send_text(f"{response}")
    #await websocket.close()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/chat/{message:path}")
def chat(message: str):
    response = agent_2.chat(message)
    return str(response)