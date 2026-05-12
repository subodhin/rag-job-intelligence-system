from pydantic import BaseModel

class IntentResponse(BaseModel):
    intent: str