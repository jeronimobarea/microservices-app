# Python
from datetime import datetime

# Sql Alchemy
from sqlalchemy import Column, String, DateTime, Boolean

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

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex)
    email = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    creation_date = Column(DateTime, default=datetime.utcnow())
    last_modification = Column(DateTime, default=datetime.utcnow())

    __mapper_args__ = {
        'polymorphic_identity': 'profiles'
    }
