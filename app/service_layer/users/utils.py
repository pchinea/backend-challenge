import contextlib

from app.adapters.db.session import get_async_session, get_user_db
from app.domain.users import UserCreate
from app.service_layer.users.config import get_user_manager
from fastapi_users.exceptions import UserAlreadyExists

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_super_user(email: str, password: str):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email, password=password, is_superuser=True
                        )
                    )
                    return True
    except UserAlreadyExists:
        return False
