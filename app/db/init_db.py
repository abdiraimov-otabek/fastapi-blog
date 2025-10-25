import asyncio

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from alembic import command
from alembic.config import Config
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.crud import create_user
from app.db.session import engine


async def init_db():
    """Initialize database with tables and superuser."""

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    print("Tables created ✅")

    # Create superuser
    async with AsyncSession(engine) as session:
        try:
            result = await session.exec(
                select(User).where(User.email == settings.FIRST_SUPERUSER)
            )
            user = result.first()

            if not user:
                await create_user(
                    session,
                    UserCreate(
                        username="admin",
                        email=settings.FIRST_SUPERUSER,
                        password=settings.FIRST_SUPERUSER_PASSWORD,
                        is_superuser=True,
                    ),
                )
                await session.commit()
                print("Superuser created ✅")
            else:
                print("Superuser already exists ✔️")
        except Exception as e:
            print(f"Error creating superuser: {e}")
            await session.rollback()


async def init_alembic():
    """Stamp the database with the current Alembic version."""
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg, "head")
    print("Alembic stamped to head ✅")


if __name__ == "__main__":
    asyncio.run(init_db())
    # Optionally stamp alembic so it knows the current version
    # asyncio.run(init_alembic())
