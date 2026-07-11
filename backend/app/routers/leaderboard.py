from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/api", tags=["leaderboard"])


@router.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(
    db: Session = Depends(get_db), user: models.User = Depends(get_current_user)
):
    return crud.leaderboard(db, user)
