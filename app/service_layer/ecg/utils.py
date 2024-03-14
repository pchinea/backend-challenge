import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.repositories.ecg import ECGRepository
from app.domain.ecg import ECG, ProcessedECG, ProcessedLead, Insights
from app.service_layer.ecg.logic import calculate_zero_crossing


async def process_ecg(db: AsyncSession, ecg: ECG, owner_id: uuid.UUID):
    """
    Receives an ECG, processes it, and stores it.

    :param db: Database session.
    :param ecg: EGC object.
    :param owner_id: UUID of the user who upload the ECG.
    :return: A ProcessedECG object with all ECG data.
    """
    proc_ecg = ProcessedECG(**ecg.model_dump(exclude={"leads"}), leads=[], owner_id=owner_id)
    for lead in ecg.leads:
        zero_crossing = calculate_zero_crossing(lead.signal)
        proc_lead = ProcessedLead(
            **lead.model_dump(),
            insights=Insights(number_of_zero_crossing=zero_crossing)
        )
        proc_ecg.leads.append(proc_lead)

    return await ECGRepository.add_ecg(db, proc_ecg)


async def get_ecg_insights(db: AsyncSession, ecg_id: uuid.UUID):
    """
    Returns ECG Insights for the given ECG id.

    :param db: Database session.
    :param ecg_id: UUID of the requested ECG.
    :return: A ProcessedECG object with all ECG data.
    """
    return await ECGRepository.get_ecg_insights(db, ecg_id)
