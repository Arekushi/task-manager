from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from src.domain.models.task import TaskStatusEnum


class Validate:
    @classmethod
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError(f'{v} cannot be empty')
        return v.strip()
    
    @classmethod
    def valid_status(cls, v):
        if str(v).lower() not in [str(status.value).lower() for status in TaskStatusEnum]:
            raise ValueError('Invalid status')
        return v


class TaskCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    description: str
    status: str
    
    @field_validator('title', 'description')
    def not_empty(cls, v):
        return Validate.not_empty(v)
    
    @field_validator('status')
    def valid_status(cls, v):
        return Validate.valid_status(v)


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    
    @field_validator('status')
    def valid_status(cls, v):
        return Validate.valid_status(v)
