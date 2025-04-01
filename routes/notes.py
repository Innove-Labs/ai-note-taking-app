from typing import Optional, List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from schemas import NoteResponse, NoteCreate
from models import Note, User
from utils.password import get_current_user

router = APIRouter()


@router.post("/", response_model=NoteResponse)
async def create_note(note_data: NoteCreate, user: User = Depends(get_current_user)):
    """Create a new note"""
    note = Note(
        user_id=user.id,
        notebook_id=note_data.notebook_id,
        title=note_data.title,
        content=note_data.content,
        summary=note_data.summary,
        audio_files=note_data.audio_files,
        tags=note_data.tags,
        note_type=note_data.note_type,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    await note.create()
    return note

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: PydanticObjectId, _= Depends(get_current_user)):
    """Fetch a note by its ID"""
    note = await Note.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.get("/", response_model= List[NoteResponse])
async def list_notes(notebook_id: Optional[str] = None, user: User = Depends(get_current_user)):
    """List all notes for a user, optionally filtered by notebook"""
    query = Note.user_id == user.id
    if notebook_id:
        query &= Note.notebook_id == notebook_id
    notes = await Note.find(query).to_list()
    return notes

@router.patch("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: PydanticObjectId, note_data: NoteCreate, _= Depends(get_current_user)):
    """Update a note"""
    note = await Note.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = note_data.title
    note.content = note_data.content
    note.summary = note_data.summary
    note.audio_files = note_data.audio_files
    note.tags = note_data.tags
    note.note_type = note_data.note_type
    note.updated_at = datetime.utcnow()

    await note.save()
    return note

@router.delete("/{note_id}")
async def delete_note(note_id: PydanticObjectId, _= Depends(get_current_user)):
    """Delete a note"""
    note = await Note.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await note.delete()
    return {"message": "Note deleted successfully"}