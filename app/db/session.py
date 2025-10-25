from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

# Create async engine (note the +aiosqlite or +asyncpg)
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True,
)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
