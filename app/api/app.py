from fastapi import Depends, FastAPI

from app.api.router import router as ecg_router
from app.domain.users import UserCreate, UserRead
from app.service_layer.users.config import auth_backend, fastapi_users, current_active_superuser


app = FastAPI()

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
