from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.athlete import Athlete
from app.schemas.athlete import AthleteCreate, AthleteUpdate, AthleteOut
from app.core.security import require_role

router = APIRouter(prefix="/athletes", tags=["athletes"])

@router.post("", response_model=AthleteOut, dependencies=[Depends(require_role("admin"))])
async def create_athlete(payload: AthleteCreate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Athlete).where(Athlete.email == payload.email))
    if q.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    athlete = Athlete(**payload.model_dump())
    db.add(athlete)
    await db.commit()
    await db.refresh(athlete)
    return athlete

@router.get("", response_model=list[AthleteOut])
async def list_athletes(
    db: AsyncSession = Depends(get_db),
    q: str | None = None,
    division: str | None = Query(None, pattern="^(Rx|Scaled)$"),
    gender: str | None = Query(None, pattern="^(Male|Female)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    stmt = select(Athlete)
    if q:
        from sqlalchemy import or_
        stmt = stmt.where(or_(Athlete.name.ilike(f"%{q}%"), Athlete.email.ilike(f"%{q}%")))
    if division:
        stmt = stmt.where(Athlete.division == division)
    if gender:
        stmt = stmt.where(Athlete.gender == gender)
    stmt = stmt.order_by(Athlete.created_at.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/{athlete_id}", response_model=AthleteOut)
async def get_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.get(Athlete, athlete_id)
    if not res:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    return res

@router.patch("/{athlete_id}", response_model=AthleteOut, dependencies=[Depends(require_role("admin"))])
async def update_athlete(athlete_id: int, payload: AthleteUpdate, db: AsyncSession = Depends(get_db)):
    athlete = await db.get(Athlete, athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(athlete, k, v)
    await db.commit()
    await db.refresh(athlete)
    return athlete

@router.delete("/{athlete_id}", status_code=204, dependencies=[Depends(require_role("admin"))])
async def delete_athlete(athlete_id: int, db: AsyncSession = Depends(get_db)):
    athlete = await db.get(Athlete, athlete_id)
    if not athlete:
        return
    await db.delete(athlete)
    await db.commit()