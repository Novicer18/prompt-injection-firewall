from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    user_id: str
    prompt: str

class FirewallResponse(BaseModel):
    is_safe: bool
    risk_score: float
    analysis: str
    ai_response: Optional[str] = None