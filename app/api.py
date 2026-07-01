from fastapi import APIRouter
from orchestrator import Orchestrator
from models.request_models import PromptRequest
from agents.observability_agent import ObservabilityAgent
from models.response_models import AgentTraceResponse

router = APIRouter()

#  global singleton Orchestrator for running multi agent system
orchestrator = Orchestrator()
observability_agent = ObservabilityAgent()

@router.post("/multi-agent/gatekeeper")
def multi_agent_pipeline(request: PromptRequest):
    return orchestrator.run(request.prompt)


##########################################################
# OBSERVABILITY ENDPOINT
##########################################################

@router.get("/observability/scores")
def get_diligence_scores():

    return observability_agent.project_scores()
