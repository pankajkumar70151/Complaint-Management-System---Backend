from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
from typing import List, Optional
from pydantic import BaseModel, Field

class ComplaintStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"

class ComplaintBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example="Damaged screen on delivery",
        description="Short title of the complaint"
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        example="The laptop arrived with a cracked screen. I need a replacement.",
        description="Detailed description of the issue"
    )
    user_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example="John Doe",
        description="Name of the user filing the complaint"
    )

class ComplaintCreate(ComplaintBase):
    """Schema for creating a new complaint."""
    pass

class ComplaintUpdateStatus(BaseModel):
    """Schema for updating the status of a complaint."""
    status: ComplaintStatus = Field(..., example="In Progress")

class ComplaintInDB(ComplaintBase):
    id: UUID = Field(default_factory=uuid4, example="123e4567-e89b-12d3-a456-426614174000")
    status: ComplaintStatus = Field(default=ComplaintStatus.OPEN, example="Open")
    created_at: datetime = Field(default_factory=datetime.utcnow, example="2024-01-01T12:00:00Z")
    updated_at: datetime = Field(default_factory=datetime.utcnow, example="2024-01-01T12:00:00Z")

    class Config:
        from_attributes = True  # Pydantic v2: allow ORM-style objects

class PaginatedComplaints(BaseModel):
    total: int = Field(..., example=42)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
    items: List[ComplaintInDB]

class AllComplaints(BaseModel):
    total: int = Field(..., example=42) 
    items: List[ComplaintInDB]