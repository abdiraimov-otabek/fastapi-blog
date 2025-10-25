from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.exec(select(User).where(User.email == email))  # Changed to exec
    user = result.first()
    return user


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    hashed_password = hash_password(user_create.password)

    user = User(
        username=user_create.username,
        email=user_create.email,
        password=hashed_password,
        is_superuser=getattr(user_create, "is_superuser", False),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
