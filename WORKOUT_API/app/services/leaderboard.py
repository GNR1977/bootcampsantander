from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.score import Score
from app.models.athlete import Athlete

async def get_leaderboard(db: AsyncSession, division: str | None = None, gender: str | None = None):
    # soma de pontos por atleta
    stmt = (
        select(
            Athlete.id,
            Athlete.name,
            Athlete.division,
            Athlete.gender,
            func.coalesce(func.sum(Score.points), 0.0).label("total_points")
        )
        .join(Score, Score.athlete_id == Athlete.id, isouter=True)
        .group_by(Athlete.id)
        .order_by(func.coalesce(func.sum(Score.points), 0.0).desc())
    )
    if division:
        from sqlalchemy import and_
        stmt = stmt.where(Athlete.division == division)
    if gender:
        stmt = stmt.where(Athlete.gender == gender)

    res = await db.execute(stmt)
    rows = res.all()
    return [
        {
            "athlete_id": r[0],
            "name": r[1],
            "division": r[2],
            "gender": r[3],
            "total_points": float(r[4] or 0.0),
        } for r in rows
    ]