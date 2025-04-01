from beanie import Document
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class NoteType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"

class Notebook(Document):
    user_id: str  # Owner of the notebook
    name: str  # Notebook title (e.g., "Meeting Notes", "Project X")
    description: Optional[str]  # Short description
    team_id: Optional[str]
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        collection = "notebooks"

class AudioFiles(BaseModel):
    storage_link: str
    created_at: datetime = datetime.utcnow()

class Note(Document):
    user_id: str
    team_id: Optional[str]
    notebook_id: Optional[str]  # Reference to a Notebook
    title: str
    content: Optional[str]  # Markdown
    summary: Optional[str] # Markdown
    audio_files: Optional[List[AudioFiles]]
    tags: List[str] = []
    note_type: NoteType = NoteType.TEXT
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        collection = "notes"
