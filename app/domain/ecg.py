import uuid

from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class LeadName(str, Enum):
    I = "I"
    II = "II"
    III = "III"
    AVR = "aVR"
    AVL = "aVL"
    AVF = "aVF"
    V1 = "V1"
    V2 = "V2"
    V3 = "V3"
    V4 = "V4"
    V5 = "V5"
    V6 = "V6"


class Lead(BaseModel):
    name: LeadName
    number_of_samples: Optional[int] = None
    signal: List[int]

    model_config = ConfigDict(from_attributes=True)


class ECG(BaseModel):
    id: uuid.UUID
    date: datetime
    leads: List[Lead]

    model_config = ConfigDict(from_attributes=True)


# Processed models

class Insights(BaseModel):
    number_of_zero_crossing: int

    model_config = ConfigDict(from_attributes=True)


class ProcessedLead(Lead):
    insights: Insights


class ProcessedECG(ECG):
    leads: List[ProcessedLead]
    owner_id: uuid.UUID
