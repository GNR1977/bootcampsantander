from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.score import Score
from app.models.wod import WOD

async def recalc_points_for_wod(db: AsyncSession, wod_id: int) -> None:
    # Carrega o WOD e decide critério
    wod = await db.get(WOD, wod_id)
    if not wod:
        return
    res = await db.execute(select(Score).where(Score.wod_id == wod_id))
    scores = list(res.scalars().all())

    # Ordenação por tipo:
    if wod.scoring_type == "for_time":
        # Menor tempo é melhor; tie-break menor é melhor
        scores.sort(key=lambda s: (s.time_seconds if s.time_seconds is not None else 10**9,
                                   s.tie_break_seconds if s.tie_break_seconds is not None else 10**9))
    elif wod.scoring_type == "amrap":
        # Maior reps é melhor; tie-break menor é melhor
        scores.sort(key=lambda s: (-(s.reps or -1), s.tie_break_seconds if s.tie_break_seconds is not None else 10**9))
    elif wod.scoring_type == "max_load":
        # Maior carga é melhor
        scores.sort(key=lambda s: (-(s.weight_kg or -1.0)))
    else:
        # fallback
        scores.sort(key=lambda s: s.id)

    # Atribuir pontos (ex.: 100 para 1º, 95 para 2º, 90 para 3º, depois -5 até mínimo 0)
    base = 100
    step = 5
    for i, s in enumerate(scores):
        pts = max(base - step * i, 0)
        s.points = float(pts)

    await db.commit()