from fastapi import FastAPI

from models import PromptRequest
from models import PromptResponse

from agent import GatekeeperAgent

app = FastAPI(
    title="Gatekeeper Agent API"
)

agent = GatekeeperAgent()


@app.post(
    "/gatekeeper",
    response_model=PromptResponse
)
def gatekeeper(request: PromptRequest):

    result = agent.execute(request.prompt)

    return PromptResponse(
        original=request.prompt,
        cleaned=result["response"]
    )


@app.get("/")
def health():

    return {
        "status": "running"
    }
