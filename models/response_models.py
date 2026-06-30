"""
------------------------------------------------------------
Response Models (Gatekeeper AI Platform)
------------------------------------------------------------
Defines all outbound API response schemas
------------------------------------------------------------
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


##########################################################
# 1. Core Prompt Response
##########################################################

class PromptResponse(BaseModel):

    input: str
    output: str
    source: str = Field(
        ...,
        description="cache | generated | llm | agent"
    )


##########################################################
# 2. Lean Content Response
##########################################################

class LeanContentResponse(BaseModel):

    original: str
    cleaned: str


##########################################################
# 3. Constraint Response
##########################################################

class ConstraintResponse(BaseModel):

    audience: str
    length: str
    format: str
    updated_prompt: str


##########################################################
# 4. Explicit Response
##########################################################

class ExplicitResponse(BaseModel):

    role: str
    tasks: List[str]
    tools: List[str]
    updated_prompt: str


##########################################################
# 5. Cache Response
##########################################################

class CacheResponse(BaseModel):

    cached: bool
    response: Optional[str] = None
    request: Optional[str] = None
    responsetime: Optional[float] = None
    cacheddatetime: Optional[datetime] = None


##########################################################
# 6. MCP Response
##########################################################

class MCPToolResponse(BaseModel):

    tool_name: str
    result: Dict[str, Any]


##########################################################
# 7. Agent Execution Trace Response (Advanced)
##########################################################

class AgentTraceResponse(BaseModel):

    input: str
    gatekeeper: Dict[str, Any]
    refiner: Dict[str, Any]
    category: Dict[str, Any]
    llm: Dict[str, Any]
    cache: Dict[str, Any]
    observability: Dict[str, Any]
    output: str
