from datetime import datetime
from typing import List
from uuid import UUID

from app.schemas.base import Base


class SampleData(Base):
    id: UUID
    first_name: str
    last_name: str
    email: str
    role: AccountRole
    active: bool


class SampleDataList(Base):
    samples: List[SampleData]