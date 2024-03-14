import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.session import get_async_session
from app.adapters.db.tables.users import User
from app.domain.ecg import ECG, ECGInsights
from app.service_layer.ecg.utils import process_ecg, get_ecg_insights
from app.service_layer.users.config import current_active_user

router = APIRouter()


@router.post("", status_code=201, response_model=ECGInsights)
async def receive_ecg(
        ecg: ECG,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
):
    if user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not (proc_ecg := await process_ecg(db, ecg, user.id)):
        raise HTTPException(status_code=409, detail="ECG_ALREADY_EXISTS")

    return ECGInsights.model_validate(proc_ecg.model_dump(exclude={"owner_id"}))


@router.get("/{ecg_id}/insights", response_model=ECGInsights)
async def get_insights(
        ecg_id: uuid.UUID,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(get_async_session)
):
    if user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not (proc_ecg := await get_ecg_insights(db, ecg_id)):
        raise HTTPException(status_code=404, detail="ECG_NOT_FOUND")

    if proc_ecg.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return ECGInsights.model_validate(proc_ecg.model_dump(exclude={"owner_id"}))
