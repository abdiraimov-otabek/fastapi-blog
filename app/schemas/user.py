from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):  # ← Add this new schema
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Updated for Pydantic v2 (was orm_mode)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
