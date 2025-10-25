<p align="center">
  # 🚀 FastAPI Blog API
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-Backend-blue?style=flat-square" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-green?style=flat-square" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/License-Apache%202.0-lightgrey?style=flat-square" alt="License">
</p>

A modern, async-ready blog backend built with FastAPI + SQLModel + PostgreSQL.

---

## ✨ Features

- 🔐 User registration & JWT authentication
- ✏️ CRUD operations for posts
- ⚡ Fully async database operations
- 📦 Structured, maintainable folder layout
- 🛠 Alembic migrations ready
- 🏗 CI/CD ready (GitHub Actions workflow included)

---

## 🛠 Tech Stack

- **Backend:** FastAPI  
- **Database:** PostgreSQL + SQLModel + AsyncPG  
- **Migrations:** Alembic  
- **CI/CD:** GitHub Actions  

---

## 🚀 Quick Start

Clone the repo:

```bash
git clone https://github.com/abdiraimov-otabek/fastapi-blog.git
cd fastapi-blog
````

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install .
```

Run the app:

```bash
uv run app.main:app --reload
```

Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔑 Environment Variables

```env
DATABASE_URL=postgresql+asyncpg://<user>:<password>@localhost:5432/<db_name>
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🗄 Database Setup

1. Make sure PostgreSQL is running.
2. Run migrations:

```bash
uv run alembic upgrade head
```

Tables for `users` and `posts` will be created automatically.

---

## 📡 API Endpoints

### Auth

* `POST /api/v1/auth/register` – Register new user
* `POST /api/v1/auth/login` – Login & get JWT

### Users

* `GET /api/v1/users/me` – Current user info
* `GET /api/v1/users/{user_id}` – Get user by ID

### Posts

* `GET /api/v1/posts` – List all posts
* `POST /api/v1/posts` – Create post
* `GET /api/v1/posts/{post_id}` – Get post by ID
* `PUT /api/v1/posts/{post_id}` – Update post
* `DELETE /api/v1/posts/{post_id}` – Delete post

*All endpoints are async-ready.*

---

## 📂 Project Structure

```
fastapi-blog/
├── app/
│   ├── api/        # Routes & dependencies
│   ├── core/       # Config & security
│   ├── db/         # Database session & initialization
│   ├── models/     # SQLModel ORM models
│   ├── schemas/    # Pydantic schemas
│   └── services/   # CRUD logic
├── alembic/        # Database migrations
├── pyproject.toml  # Dependencies
├── uv.lock         # uv lockfile
└── README.md
```
