from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

class AgentBase(BaseModel):
    agent_id: str = Field(..., example="fashion_stylist_v1")
    name: str = Field(..., example="Fashion Stylist Agent")
    description: Optional[str] = Field(None, example="Provides clothing and outfit recommendations")
    version: str = Field("1.0.0", example="1.0.0")
    input_schema: Dict[str, Any] = Field(..., example={"type": "object", "properties": {}})
    output_schema: Dict[str, Any] = Field(..., example={"type": "object", "properties": {}})
    is_active: bool = Field(True, example=True)

class AgentRegister(AgentBase):
    pass

class AgentResponse(AgentBase):
    id: int
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

class AgentList(BaseModel):
    agents: List[AgentResponse]
    total: int