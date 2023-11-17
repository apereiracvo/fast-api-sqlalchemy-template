from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import StringEncryptedType

from app.config import settings
from app.db.models import BaseModel

class SampleModel(BaseModel):
    __tablename__ = "sample"

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(StringEncryptedType(String(100), key), nullable=False)
    role = Column(Enum(AccountRole), nullable=False)
    active = Column(Boolean, nullable=False)
