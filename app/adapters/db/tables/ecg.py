import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import PickleType, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.db.tables.base import Base


class ECG(Base):
    __tablename__ = "ecgs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    leads: Mapped[List["Lead"]] = relationship(back_populates="ecg")
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    ecg: Mapped["ECG"] = relationship(back_populates="leads")
    ecg_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ecgs.id"))
    name: Mapped[str]
    number_of_samples: Mapped[Optional[int]]
    signal = Column('signal', PickleType)
    insights: Mapped["Insights"] = relationship(back_populates="lead")


class Insights(Base):
    __tablename__ = "insights"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lead: Mapped["Lead"] = relationship(back_populates="insights")
    lead_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("leads.id"))
    number_of_zero_crossing: Mapped[int]
