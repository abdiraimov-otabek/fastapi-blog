from typing import Generic, TypeVar, Type, Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, obj_id: UUID) -> Optional[ModelType]:
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 20
    ) -> List[ModelType]:
        result = await session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(
        self, session: AsyncSession, obj_in: CreateSchemaType
    ) -> ModelType:
        obj = self.model(**obj_in.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            if key == "id":
                continue
            setattr(db_obj, key, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, obj_id: UUID) -> Optional[ModelType]:
        db_obj = await self.get(session, obj_id)
        if not db_obj:
            return None
        await session.delete(db_obj)
        await session.commit()
        return db_obj
