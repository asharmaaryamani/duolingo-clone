from typing import Optional
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from . import crud, models
from .database import get_db


def get_current_user(
    x_user_id: Optional[str] = Header(default=None, alias="X-User-Id"),
    db: Session = Depends(get_db),
) -> models.User:
    """
    Resolves the caller's account from the X-User-Id header the frontend sends
    (a per-browser id generated on first visit, stored in localStorage).
    This is deliberately NOT real authentication -- there are no passwords or
    tokens to verify -- it simply keeps each visitor's progress separate, per
    the assignment's 'simplified auth' allowance. Falls back to the seeded
    demo account when no header is present (e.g. hitting /docs directly).
    """
    if x_user_id:
        return crud.get_or_create_user(db, x_user_id)
    return crud.get_or_create_default_user(db)
