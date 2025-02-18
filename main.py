from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import asyncio
import iask

app = FastAPI()

client = iask.Client()

async def get_streaming_response(mode: str, query: str, stream: bool):
    async for chunk in await client.ask({'mode': mode, 'q': query}, stream=stream):
        yield chunk

@app.get("/ask")
async def ask(
    mode: str = Query(default="wiki", description="Mode for the query"),
    q: str = Query(..., description="The query string"),
    stream: bool = Query(default=True, description="Whether to stream the response")
):
    return StreamingResponse(
        get_streaming_response(mode, q, stream), 
        media_type="text/plain"
    )

# Add a root route for health check
@app.get("/")
async def root():
    return {"status": "ok"}
