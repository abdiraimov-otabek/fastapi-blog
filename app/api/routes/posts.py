import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.models.post import Post
from app.schemas.post import PostCreate, PostOut, PostUpdate
from app.services.post_crud import post_crud

router = APIRouter()


@router.get("/", response_model=list[PostOut])
async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Post))
    print(result)
    return result.scalars().all()


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Post).where(Post.id == post_id))
    print(result)
    return result.scalars().one()


@router.post("/", response_model=list[PostCreate])
async def create_post(post: PostCreate, session: AsyncSession = Depends(get_session)):
    return await post_crud.create(session, post)


@router.patch("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: uuid.UUID, post: PostUpdate, session: AsyncSession = Depends(get_session)
):
    db_post = await session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return await post_crud.update(session, db_post, post)


@router.delete("/{post_id}", response_model=PostOut)
async def delete_post(post_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    db_post = await session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.delete(db_post)
    await session.commit()
    return db_post
