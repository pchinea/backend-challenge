import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from app.adapters.db.session import create_db_and_tables
from app.adapters.db.tables.users import User
from app.domain.ecg import ECG, ECGInsights
from app.domain.users import UserCreate, UserRead
from app.service_layer.ecg.utils import process_ecg, get_ecg_insights
from app.service_layer.users.config import auth_backend, current_active_user, fastapi_users, current_active_superuser
from app.service_layer.users.utils import create_super_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    await create_super_user("admin@example.com", "1234")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(current_active_superuser)]
)


@app.post("/ecg", status_code=201)
async def receive_ecg(ecg: ECG, user: User = Depends(current_active_user)):
    if user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not (proc_ecg := await process_ecg(ecg, user)):
        raise HTTPException(status_code=400, detail="ECG_ALREADY_EXISTS")

    return ECGInsights.model_validate(proc_ecg)


@app.get("/ecg/{ecg_id}/insights")
async def get_insights(ecg_id: uuid.UUID, user: User = Depends(current_active_user)):
    if user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not (proc_ecg := await get_ecg_insights(ecg_id)):
        raise HTTPException(status_code=404, detail="ECG_NOT_FOUND")

    if proc_ecg.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return ECGInsights.model_validate(proc_ecg)
