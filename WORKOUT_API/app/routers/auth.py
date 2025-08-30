from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.email == form_data.username))
    user = q.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    access = create_access_token(sub=user.email, role=user.role)
    refresh = create_refresh_token(sub=user.email)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token inválido")
    sub = payload["sub"]
    # role deveria ser buscada no BD
    # por simplicidade, role = viewer
    access = create_access_token(sub=sub, role="viewer")
    return {"access_token": access, "token_type": "bearer"}