# Python
from datetime import datetime

# Sql Alchemy
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey

# Database
from src.database import Base

# Uuid
import uuid


# Models
class Profile(Base):
    """
    Profile SQL Alchemy class
    """
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    device_id = Column(String, nullable=True)
    image = Column(String, nullable=True)
    cover = Column(String, nullable=True)
    email = Column(String, unique=True)
    username = Column(String, nullable=True, default=email)
    description = Column(String, nullable=True)
    web = Column(String, nullable=True)
    is_verified = Column(String, nullable=True, default=False)
    is_active = Column(Boolean, default=True, nullable=True)
    creation_date = Column(DateTime, default=datetime.utcnow())
    last_modification = Column(DateTime, default=datetime.utcnow())
