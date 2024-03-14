import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.tables.ecg import ECG, Lead, Insights
from app.domain.ecg import ProcessedECG


class ECGRepository:
    @staticmethod
    async def add_ecg(db: AsyncSession, ecg: ProcessedECG):
        """
        Stores a processed ECG into the database.

        :param db: Database session.
        :param ecg: Processed ECG.
        :return: Processed ECG or None if the ECG already exists.
        """
        db_ecg = ECG(**ecg.model_dump(exclude={"leads"}))
        for lead in ecg.leads:
            db_lead = Lead(**lead.model_dump(exclude={"insights"}))
            db_lead.insights = Insights(**lead.insights.model_dump())
            db_ecg.leads.append(db_lead)
        try:
            db.add(db_ecg)
            await db.commit()
        except IntegrityError:
            return None
        return ProcessedECG.model_validate(db_ecg)

    @staticmethod
    async def get_ecg_insights(db: AsyncSession, ecg_id: uuid.UUID):
        """
        Retrieves ECG data form the database.

        :param db: Database session.
        :param ecg_id: UUID of the requested ECG.
        :return: Processed ECG or None if it does not exist.
        """
        if db_ecg := await db.get(ECG, ecg_id):
            return ProcessedECG.model_validate(db_ecg)
        return None
