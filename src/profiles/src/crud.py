# Fast Api
from fastapi.encoders import jsonable_encoder

# Sql Alchemy
from sqlalchemy.orm import Session

# Schemas and Models
from src import models, schemas

# Utils
from datetime import datetime

# CRUD methods
from src.utils import get_paginator


def get_profile(db: Session, profile_id: str):
    """
    Get's a profile id and return's the object that matches
    :param db:
    :param profile_id:
    :return:
    """
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()


def get_profile_by_email(db: Session, email: str):
    """
    Get's a profile email and return's the object that matches
    :param db:
    :param email:
    :return:
    """
    return db.query(models.Profile).filter(models.Profile.email == email).first()


def get_profiles(db: Session, page: int = 1, per_page: int = 10, ):
    """
    Send's a list with all profiles
    :param db:
    :param page:
    :param per_page:
    :return:
    """
    item_list = db.query(models.Profile).all()
    query = db.query(models.Profile).offset(page).limit(per_page).all()
    pagination = get_paginator(page=page, per_page=per_page, item_list=item_list, query=query)
    return pagination


def get_active_profiles(db: Session, page: int = 1, per_page: int = 10, ):
    """
    Send's a list with the active profiles
    :param db:
    :param page:
    :param per_page:
    :return:
    """
    is_active = True
    item_list = db.query(models.Profile).all()
    query = db.query(models.Profile).filter(models.Profile.is_active == is_active).offset(page).limit(per_page).all()
    pagination = get_paginator(page=page, per_page=per_page, item_list=item_list, query=query)
    return pagination


def get_inactive_profiles(db: Session, page: int = 1, per_page: int = 10, ):
    """
    Send's a list with inactive profiles
    :param db:
    :param page:
    :param per_page:
    :return:
    """
    is_active = False
    item_list = db.query(models.Profile).all()
    query = db.query(models.Profile).filter(models.Profile.is_active == is_active).offset(page).limit(per_page).all()
    pagination = get_paginator(page=page, per_page=per_page, item_list=item_list, query=query)
    return pagination


def create_profile(db: Session, profile: schemas.ProfileCreate):
    """
    Get's a profile schema and create's an object with the schema's data
    :param db:
    :param profile:
    :return:
    """
    db_profile = models.Profile(email=profile.email, is_active=True)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    # backup_service = ''
    # response = requests.post(url=backup_service, data=jsonable_encoder(db_profile))
    return db_profile


def update_profile(db: Session, profile: schemas.Profile):
    """
    1º Get de model from de database and map it.
    2º Take that model and parse with the schema that we want.
    3º Exclude de fields that are empty.
    4º Assign the new data to the existent schema.
    5º Get the raw model and add the fields.
    :param db:
    :param profile:
    :return:
    """
    stored_profile_data = jsonable_encoder(db.query(models.Profile).filter(models.Profile.id == profile.id).first())
    stored_profile_model = schemas.Profile(**jsonable_encoder(stored_profile_data))

    update_data = profile.dict(exclude_unset=True)
    updated_profile = stored_profile_model.copy(update=update_data)
    stored = db.query(models.Profile).filter(models.Profile.id == profile.id).first()

    stored.first_name = updated_profile.first_name
    stored.last_name = updated_profile.last_name
    stored.email = updated_profile.email
    stored.birthday = updated_profile.birthday
    stored.description = updated_profile.description
    stored.name = updated_profile.name
    stored.web = updated_profile.web
    stored.is_company = updated_profile.is_company
    stored.last_modification = datetime.utcnow()

    db.commit()
    return updated_profile


def deactivate(db: Session, profile_id: str):
    """
    Set the is_active var to False
    :param db:
    :param profile_id:
    :return:
    """
    stored_profile_data = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    stored_profile_data.is_active = False

    db.commit()
    db.refresh(stored_profile_data)
    return jsonable_encoder(stored_profile_data)


def activate(db: Session, profile_id: str):
    """
    Set the is_active var to True
    :param db:
    :param profile_id:
    :return:
    """
    stored_profile_data = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    stored_profile_data.is_active = True

    db.commit()
    db.refresh(stored_profile_data)
    return jsonable_encoder(stored_profile_data)
