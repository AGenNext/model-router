from pydantic import BaseModel
from typing import List, Literal


class Message(BaseModel):
    role: str
    content: str


class RouteRequest(BaseModel):
    messages: List[Message]
    objective: Literal["balanced", "speed", "quality", "cost", "reliability"] = "balanced"
    required_capabilities: List[str] = []
    max_budget_usd: float = 1.0
