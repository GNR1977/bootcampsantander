from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.leaderboard import get_leaderboard

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("")
async def leaderboard(
    db: AsyncSession = Depends(get_db),
    division: str | None = Query(None, pattern="^(Rx|Scaled)$"),
    gender: str | None = Query(None, pattern="^(Male|Female)$"),
):
    return await get_leaderboard(db, division=division, gender=gender)