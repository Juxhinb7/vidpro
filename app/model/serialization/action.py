from pydantic import BaseModel

class ActionResponse(BaseModel):
    message: str