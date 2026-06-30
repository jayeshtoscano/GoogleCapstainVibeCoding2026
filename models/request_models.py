"""
------------------------------------------------------------
Request Models (Gatekeeper AI Platform)
------------------------------------------------------------
Defines all inbound API request schemas
------------------------------------------------------------
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


##########################################################
# 1. Core Prompt Request
##########################################################

class PromptRequest(BaseModel):

    prompt: str = Field(
        ...,
        description="Raw user input prompt"
    )

    user_id: Optional[str] = Field(
        None,
        description="Optional user identifier for tracking"
    )

    session_id: Optional[str] = Field(
        None,
        description="Session context for multi-turn workflows"
    )


##########################################################
# 2. Generic Text Request
##########################################################

class TextRequest(BaseModel):

    text: str = Field(
        ...,
        description="Input text for processing"
    )


##########################################################
# 3. Cache Write Request
##########################################################

class CacheRequest(BaseModel):

    request: str
    response: str
    responsetime: float
    cacheddatetime: datetime


##########################################################
# 4. MCP Tool Call Request
##########################################################

class MCPToolRequest(BaseModel):

    tool_name: str
    payload: Dict[str, Any]


##########################################################
# 5. Agent Execution Request (Advanced)
##########################################################

class AgentRequest(BaseModel):

    prompt: str
    enable_cache: bool = True
    enable_refiner: bool = True
    enable_observability: bool = True

    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict
    )
