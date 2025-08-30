from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.score import Score
from app.models.athlete import Athlete
from app.models.wod import WOD
from app.schemas.score import ScoreCreate, ScoreOut
from app.core.security import require_role
from app.services.scoring import recalc_points_for_wod

router = APIRouter(prefix="/scores", tags=["scores"])

@router.post("", response_model=ScoreOut, dependencies=[Depends(require_role("judge","admin"))])
async def submit_score(payload: ScoreCreate, bg: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    # valida relações
    if not await db.get(Athlete, payload.athlete_id):
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    wod = await db.get(WOD, payload.wod_id)
    if not wod:
        raise HTTPException(status_code=404, detail="WOD não encontrado")

    # regra: preencher somente campos do tipo correto
    if wod.scoring_type == "for_time" and payload.time_seconds is None:
        raise HTTPException(status_code=422, detail="time_seconds é obrigatório para for_time")
    if wod.scoring_type == "amrap" and payload.reps is None:
        raise HTTPException(status_code=422, detail="reps é obrigatório para amrap")
    if wod.scoring_type == "max_load" and payload.weight_kg is None:
        raise HTTPException(status_code=422, detail="weight_kg é obrigatório para max_load")

    score = Score(**payload.model_dump())
    db.add(score)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe score para este atleta neste WOD")
    await db.refresh(score)

    # recalcular pontos no background
    bg.add_task(recalc_points_for_wod, db, payload.wod_id)
    return score

@router.get("/by_wod/{wod_id}", response_model=list[ScoreOut])
async def scores_by_wod(wod_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Score).where(Score.wod_id == wod_id))
    return res.scalars().all()