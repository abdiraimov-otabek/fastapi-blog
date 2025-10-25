from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_current_user, get_current_superuser
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user


@router.get("/", response_model=list[UserOut])
async def list_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_superuser),  # Only superusers
):
    """List all users (superuser only)"""
    from sqlmodel import select

    result = await session.exec(select(User))
    return result.all()
