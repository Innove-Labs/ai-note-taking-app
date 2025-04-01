from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Enums for Note Types
class NoteType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"

# Schema for creating/updating a Notebook
class NotebookCreate(BaseModel):
    name: str
    description: Optional[str]
    team_id: Optional[str]

class NotebookResponse(NotebookCreate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema for audio file references
class AudioFiles(BaseModel):
    storage_link: str
    created_at: datetime = datetime.utcnow()

# Schema for creating/updating a Note
class NoteCreate(BaseModel):
    notebook_id: Optional[str]
    title: str
    content: Optional[str]  # Markdown
    summary: Optional[str]
    audio_files: Optional[List[AudioFiles]]
    tags: List[str] = []
    note_type: NoteType = NoteType.TEXT

class NoteResponse(NoteCreate):
    id: str
    user_id: str
    team_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
