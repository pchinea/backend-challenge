from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.adapters.db.session import create_db_and_tables
from app.api.router import router as ecg_router
from app.domain.users import UserCreate, UserRead
from app.service_layer.users.config import auth_backend, fastapi_users, current_active_superuser
from app.service_layer.users.utils import create_super_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    await create_super_user("admin@example.com", "1234")
    yield


app = FastAPI(lifespan=lifespan)

# Users router
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(current_active_superuser)]
)

# ECGs router
app.include_router(ecg_router, prefix="/ecg", tags=["ecg"])
