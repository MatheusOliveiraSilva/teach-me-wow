import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import AsyncGenerator

from apps.teacher_agent.agent.agent_streaming import AgentStreaming
from apps.teacher_agent.agent.agent_state import AgentState
from apps.teacher_agent.api.schemas.chat_schemas import ChatRequest
from apps.teacher_agent.api.db.database import get_db

from langchain_core.messages import HumanMessage

router = APIRouter(
    prefix="/agent",
    tags=["Agent Interaction"],
)

agent_streamer = AgentStreaming()

@router.post("/chat/stream")
def stream_agent_chat(
    chat_request: ChatRequest,
    # db: Session = Depends(get_db) # Descomente quando for usar o DB
):
    """
    Receives a user message and LLM config, streams the agent's response using SSE.
    """
    try:
        global agent_streamer
        
        initial_agent_state: AgentState = {
            "messages": [HumanMessage(content=chat_request.message.content)],
            "llm_config": chat_request.llm_config.model_dump()
        }
        
        return StreamingResponse(agent_streamer.stream(initial_agent_state), media_type="text/event-stream")

    except Exception as e:
        print(f"Error in stream_agent_chat: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
