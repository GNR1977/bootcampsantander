from pydantic import BaseModel, EmailStr, Field

class AthleteBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    division: str = Field(..., pattern="^(Rx|Scaled)$")
    gender: str = Field(..., pattern="^(Male|Female)$")

class AthleteCreate(AthleteBase):
    pass

class AthleteUpdate(BaseModel):
    name: str | None = None
    division: str | None = None
    gender: str | None = None

class AthleteOut(AthleteBase):
    id: int

    model_config = {
        "from_attributes": True
    }