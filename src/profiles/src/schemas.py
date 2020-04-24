# Datetime
from datetime import datetime

# Pydantic
from pydantic import BaseModel

# Utils
from typing import Optional, List

from pydantic import BaseModel as PydanicModel

"""
Here we declare all the schemas that we want for retrieving data from 
the Profile model
"""


# Models


class ProfileBase(BaseModel):
    email: str


class ProfileCreate(ProfileBase):
    pass


class BasicProfile(BaseModel):
    id: str
    image: Optional[str] = None
    first_name: Optional[str] = None

    class Config:
        orm_mode = True


class Profile(ProfileBase):
    id: str
    image: Optional[str] = None
    cover: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[datetime] = None
    description: Optional[str] = None
    is_company: Optional[bool] = None
    web: Optional[str] = None
    name: Optional[str] = None
    creation_date: Optional[datetime]
    last_modification: Optional[datetime]

    class Config:
        orm_mode = True


class ProfileDelete(BaseModel):
    is_active: bool = False


class Pagination(PydanicModel):
    page: int
    per_page: Optional[int]
    total_pages: Optional[int]
    has_next: Optional[bool]
    has_prev: Optional[bool]
    results: Optional[List[Profile]]
