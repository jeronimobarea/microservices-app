# Datetime
from datetime import datetime

# Pydantic
from pydantic import BaseModel

# Utils
from typing import Optional, List

"""
Here we declare all the schemas that we want for retrieving data from 
the Profile model
"""


# Models
class ProfileBase(BaseModel):
    email: str


class ProfileCreate(ProfileBase):
    device_id: Optional[str]
    pass


class BasicProfile(BaseModel):
    id: str
    image: Optional[str] = None
    username: Optional[str] = None
    device_id: Optional[str] = None

    class Config:
        orm_mode = True


class Profile(ProfileBase):
    id: str
    device_id: Optional[str]
    image: Optional[str]
    cover: Optional[str]
    email: Optional[str]
    username: Optional[str]
    description: Optional[str]
    web: Optional[str]
    is_verified: Optional[bool]
    creation_date: Optional[datetime]
    last_modification: Optional[datetime]

    class Config:
        orm_mode = True


class ProfileStatus(BaseModel):
    is_active: bool


class Pagination(BaseModel):
    page: int
    per_page: Optional[int]
    total_pages: Optional[int]
    has_next: Optional[bool]
    has_prev: Optional[bool]
    results: Optional[List[Profile]]
