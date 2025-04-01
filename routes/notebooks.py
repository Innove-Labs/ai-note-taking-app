from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List

from schemas import NotebookResponse, NotebookCreate
from models import Notebook
from utils.password import get_current_user
from models import User

router = APIRouter()

@router.post("/", response_model=NotebookResponse)
async def create_notebook(notebook_data: NotebookCreate, user: User = Depends(get_current_user)):
    """Create a new notebook for a user"""
    notebook = Notebook(
        user_id=user.id,
        name=notebook_data.name,
        description=notebook_data.description,
        team_id=notebook_data.team_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    await notebook.create()
    return notebook

@router.get("/{notebook_id}", response_model=NotebookResponse)
async def get_notebook(notebook_id: PydanticObjectId, _ = Depends(get_current_user)):
    """Fetch a notebook by its ID"""
    notebook = await Notebook.get(notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return notebook

@router.get("/", response_model=List[NotebookResponse])
async def list_notebooks(user_id: str, _ = Depends(get_current_user)):
    """Get all notebooks for a user"""
    notebooks = await Notebook.find(Notebook.user_id == user_id).to_list()
    return notebooks

@router.patch("/{notebook_id}", response_model=NotebookResponse)
async def update_notebook(notebook_id: PydanticObjectId, notebook_data: NotebookCreate, _ = Depends(get_current_user)):
    """Update a notebook"""
    notebook = await Notebook.get(notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    notebook.name = notebook_data.name
    notebook.description = notebook_data.description
    notebook.updated_at = datetime.utcnow()

    await notebook.save()
    return notebook

@router.delete("/{notebook_id}")
async def delete_notebook(notebook_id: PydanticObjectId, _ = Depends(get_current_user)):
    """Delete a notebook"""
    notebook = await Notebook.get(notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")

    await notebook.delete()
    return {"message": "Notebook deleted successfully"}
