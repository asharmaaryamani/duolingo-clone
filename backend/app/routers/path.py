from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/api", tags=["path"])


@router.get("/path", response_model=schemas.PathOut)
def get_path(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return crud.build_path(db, user)
