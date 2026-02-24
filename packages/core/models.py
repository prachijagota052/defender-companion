from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ThreatAlert(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    source_type: str
    file_path: Optional[str] = None
    threat_name: Optional[str] = None
    action_taken: Optional[str] = None
    severity: Optional[str] = None
    raw_message: Optional[str] = None


class UserAlert(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    title: str
    why_blocked: str
    explanation: str
    recommended_steps: List[str]
    severity: str
    file_path: Optional[str] = None
    threat_name: Optional[str] = None
    source_type: Optional[str] = None
