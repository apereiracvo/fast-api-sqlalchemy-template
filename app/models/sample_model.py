from sqlalchemy import Boolean, Column, Enum, String
from sqlalchemy_utils import StringEncryptedType

from app.config import settings
from app.db.models import BaseModel


key = settings.DB_AES_ENC_KEY


class SampleModel(BaseModel):
    __tablename__ = "sample"

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(StringEncryptedType(String(100), key), nullable=False)
    active = Column(Boolean, nullable=False)
