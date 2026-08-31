from pydantic import BaseModel

class AskRequest(BaseModel):
    query: str


class ContextAgentRequest(BaseModel):

    user_id: str
    query: str