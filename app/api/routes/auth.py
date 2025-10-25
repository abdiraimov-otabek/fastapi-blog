from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.db.session import get_session
from app.api.deps import get_current_user
from app.schemas.user import Token, UserCreate, UserLogin, UserOut
from app.models.user import User
from app.services import crud

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db, user)


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_session)):
    db_user = await crud.get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint (JWT tokens are stateless, so this is mainly for client-side cleanup)
    In production, you might want to implement token blacklisting
    """
    return {
        "message": "Logout successful",
        "detail": "Please remove the token from client storage",
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh access token
    Creates a new token for the authenticated user
    """
    new_token = create_access_token({"sub": current_user.email})
    return {"access_token": new_token, "token_type": "bearer"}
