from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.services.base import BaseCRUD

post_crud = BaseCRUD[Post, PostCreate, PostUpdate](Post)
