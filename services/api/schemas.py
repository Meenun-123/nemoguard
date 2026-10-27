from typing import Optional, List, Dict, Any, Literal
from datetime import datetime

try:
    from pydantic import BaseModel, Field
    
    class AnalyzeRequest(BaseModel):
        code: str
        language: str = "python"
        task_description: str = "Audit security vulnerabilities and generate verified patch"
        auto_verify: bool = True
        max_iterations: Optional[int] = 5

    class TaskResponse(BaseModel):
        task_id: str
        status: str
        created_at: str

    class AgentEvent(BaseModel):
        task_id: str
        step: int
        event_type: str
        message: str
        data: Optional[Dict[str, Any]] = None
        timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    class HealthResponse(BaseModel):
        status: str
        execution_mode: str
        model_id: str
        nebius_base_url: str
        max_iterations: int

except ImportError:
    from dataclasses import dataclass, field, asdict

    @dataclass
    class AnalyzeRequest:
        code: str
        language: str = "python"
        task_description: str = "Audit security vulnerabilities and generate verified patch"
        auto_verify: bool = True
        max_iterations: int = 5

        def dict(self):
            return asdict(self)

    @dataclass
    class TaskResponse:
        task_id: str
        status: str
        created_at: str

        def dict(self):
            return asdict(self)

    @dataclass
    class AgentEvent:
        task_id: str
        step: int
        event_type: str
        message: str
        data: Optional[Dict[str, Any]] = None
        timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

        def dict(self):
            return asdict(self)

    @dataclass
    class HealthResponse:
        status: str
        execution_mode: str
        model_id: str
        nebius_base_url: str
        max_iterations: int

        def dict(self):
            return asdict(self)
