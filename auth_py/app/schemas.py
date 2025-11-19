from pydantic import BaseModel, Field

class UserAuthIn(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)

class UserSignUpIn(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=6)
    surName: str
    name: str
    patronymicName: str | None = None
    jobTitle: str | None = None
    userRole: str

class UserOut(BaseModel):
    id: int
    username: str
    accessToken: str | None = None
    refreshToken: str | None = None
    class Config:
        from_attributes = True
