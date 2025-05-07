from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class LLMConfigInput(BaseModel):
    model: str = "gpt-4o"
    provider: str = "azure"

class ChatMessageInput(BaseModel):
    content: str

class ChatRequest(BaseModel):
    message: ChatMessageInput
    llm_config: LLMConfigInput