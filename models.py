from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    original: str
    cleaned: str
