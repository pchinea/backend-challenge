import contextlib

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.session import get_user_db
from app.domain.users import UserCreate
from app.service_layer.users.config import get_user_manager
from fastapi_users.exceptions import UserAlreadyExists

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(db: AsyncSession, email: str, password: str, is_superuser: bool = False):
    try:
        async with get_user_db_context(db) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                await user_manager.create(
                    UserCreate(
                        email=email, password=password, is_superuser=is_superuser
                    )
                )
                print(f"User created {email}")
    except UserAlreadyExists:
        print(f"User {email} already exists")
