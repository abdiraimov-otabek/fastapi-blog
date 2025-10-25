from fastapi import FastAPI

from app.api.router import api_router
from sqladmin import Admin, ModelView
from app.db.session import engine
from app.models.user import User
from app.models.post import Post

app = FastAPI(
    title="Blog API",
    description=(
        "A clean, modular FastAPI-based backend for managing blog posts and users. "
        "Includes async SQLModel integration, Alembic migrations, and secure JWT authentication."
    ),
    version="1.0.0",
    contact={
        "name": "Otabek Abdiraimov",
        "url": "https://github.com/otabek-abdiraimov",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "auth",
            "description": "User registration, login, and token handling",
        },
        {
            "name": "users",
            "description": "Operations for user management",
        },
        {
            "name": "posts",
            "description": "CRUD operations for blog posts",
        },
    ],
)


admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_superuser]


admin.add_view(UserAdmin)


class PostAdmin(ModelView, model=Post):
    column_list = [
        Post.id,
        Post.title,
        Post.short_description,
        Post.is_published,
        Post.created_at,
    ]


admin.add_view(PostAdmin)


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Health check completed successfully."}


app.include_router(api_router, prefix="/api/v1")
