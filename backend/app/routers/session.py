import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api", tags=["session"])


class CreateSessionIn(BaseModel):
    display_name: str = Field(min_length=1, max_length=30)


@router.post("/session", response_model=schemas.UserOut)
def create_session(payload: CreateSessionIn, db: Session = Depends(get_db)):
    """Creates a brand-new learner account (no password -- this is the
    simplified 'auth' the assignment allows). The frontend stores the
    returned username in localStorage and sends it back as X-User-Id on
    every subsequent request."""
    username = f"user_{uuid.uuid4().hex[:10]}"
    user = crud.get_or_create_user(db, username, payload.display_name)
    out = schemas.UserOut.model_validate(user)
    out.today_xp = 0
    return out
