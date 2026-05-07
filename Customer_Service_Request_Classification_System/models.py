from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON

class customerRequests(SQLModel, table = True):
    __tablename__ = "customer_requests"
    id : Optional[int] = Field(default = None, primary_key=True)
    ticket_id: str = Field(default = None)
    customer_id: str
    channel: str
    request_text: str
    created_at: str


class requestClassifications(SQLModel, table = True):
    __tablename__ = "request_classifications"
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: str = Field(default = None)
    category: str
    priority: str
    tags: List[str] = Field(sa_column=Column(JSON))
    estimated_resolution_time: int
    confidence: float
    processed_at: datetime

