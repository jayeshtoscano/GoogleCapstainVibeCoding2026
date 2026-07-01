from fastapi import APIRouter
import Orchestrator
from models.request_models import PromptRequest

router = APIRouter()

#  global singleton Orchestrator for running multi agent system
orchestrator = Orchestrator()


@router.post("/multi-agent/gatekeeper")
def multi_agent_pipeline(request: PromptRequest):
    return orchestrator.run(request.prompt)
