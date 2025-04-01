from fastapi import APIRouter
from .auth import router as auth_router
from .notes import router as notes_router
from .notebooks import router as notebook_router

router = APIRouter()

router.include_router(router=auth_router, prefix="/auth", tags=["auth"])
router.include_router(router=notes_router, prefix="/notes", tags=["notes"])
router.include_router(router=notebook_router, prefix="/notebook", tags=["notebook"])

