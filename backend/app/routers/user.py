from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/api", tags=["user"])


@router.get("/me", response_model=schemas.UserOut)
def get_me(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    user = crud.regenerate_hearts(db, user)
    out = schemas.UserOut.model_validate(user)
    out.today_xp = crud.today_xp(db, user)
    return out


@router.post("/hearts/refill", response_model=schemas.HeartsRefillOut)
def refill_hearts(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return crud.refill_hearts(db, user)


@router.post("/hearts/practice", response_model=schemas.HeartsRefillOut)
def practice_refill(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    """Mocked free 'practice' action that earns back one heart."""
    return crud.practice_refill(db, user)
