# Python
from datetime import datetime

# Sql Alchemy
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey

# Database
from src.database import Base

# Uuid
import uuid


def generate_uuid():
    return str(uuid.uuid4())


# Models
class Profile(Base):
    """
    Profile SQL Alchemy class
    """
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, unique=True, default=lambda: uuid.uuid4().hex)
    device_id = Column(String, nullable=True)
    image = Column(String, nullable=True)
    cover = Column(String, nullable=True)
    email = Column(String, unique=True)
    username = Column(String, nullable=True, default=email.split('@')[0])
    description = Column(String, nullable=True)
    web = Column(String, nullable=True)
    is_verified = Column(String, nullable=True, default=False)
    is_active = Column(Boolean, default=True, nullable=True)
    creation_date = Column(DateTime, default=datetime.utcnow())
    last_modification = Column(DateTime, default=datetime.utcnow())
