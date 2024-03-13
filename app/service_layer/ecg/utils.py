import uuid

from app.adapters.repositories.ecg import ECGRepository
from app.domain.ecg import ECG, ProcessedECG, ProcessedLead, Insights
from app.service_layer.ecg.logic import calculate_zero_crossing


async def process_ecg(ecg: ECG, user):
    proc_ecg = ProcessedECG(**ecg.model_dump(exclude={"leads"}), leads=[], owner_id=user.id)
    for lead in ecg.leads:
        zero_crossing = calculate_zero_crossing(lead.signal)
        proc_lead = ProcessedLead(
            **lead.model_dump(),
            insights=Insights(number_of_zero_crossing=zero_crossing)
        )
        proc_ecg.leads.append(proc_lead)

    return await ECGRepository.add_ecg(proc_ecg)


async def get_ecg_insights(ecg_id: uuid.UUID):
    return await ECGRepository.get_ecg_insights(ecg_id)
