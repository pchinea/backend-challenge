import contextlib

from sqlalchemy.exc import IntegrityError

from app.adapters.db.session import get_async_session
from app.adapters.db.tables.ecg import ECG, Lead, Insights
from app.domain.ecg import ProcessedECG


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


class ECGRepository:
    @staticmethod
    async def add_ecg(ecg: ProcessedECG):
        db_ecg = ECG(**ecg.model_dump(exclude={"leads"}))
        for lead in ecg.leads:
            db_lead = Lead(**lead.model_dump(exclude={"insights"}))
            db_lead.insights = Insights(**lead.insights.model_dump())
            db_ecg.leads.append(db_lead)
        try:
            async with get_async_session_context() as session:
                async with session.begin():
                    session.add(db_ecg)
        except IntegrityError:
            return False
        return True
