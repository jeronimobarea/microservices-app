# Fast Api
from fastapi import UploadFile, File
from fastapi.encoders import jsonable_encoder

# Sql Alchemy
from sqlalchemy.orm import Session

# Schemas and Models
from src import models, schemas

# Utils
import datetime
import uuid
from typing import List

# CRUD methods
from src.utils import get_paginator

# Firebase
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app-from-idea-to-code-firebase-adminsdk-ka5lc-ff4abf8221.json"

client = storage.Client().from_service_account_json("app-from-idea-to-code-firebase-adminsdk-ka5lc-ff4abf8221.json")
bucket = client.get_bucket("app-from-idea-to-code.appspot.com")


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
    db_profile = models.Profile(email=profile.email, is_active=True, username=profile.email)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def get_profile_list_by_id(profiles_id: List[str], db: Session):
    """

    :param profiles_id:
    :param db:
    :return:
    """
    data = db.query(models.Profile).filter(models.Profile.id.in_(profiles_id)).all()
    return data


def get_basic_data(db: Session, profile_id: str):
    """

    :param db:
    :param profile_id:
    :return:
    """
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    return profile


def upload_image(profile_id: str, db: Session, file: UploadFile = File(...)):
    """

    :param db:
    :param file:
    :param profile_id:
    :return:
    """
    stored = db.query(models.Profile).filter(models.Profile.id == profile_id).first()

    image_name = str(uuid.uuid4().hex) + '.png'
    image_blob = bucket.blob('profiles/pictures/' + image_name)
    image_blob.upload_from_string(
        file.file.read(),
        content_type='image/png'
    )
    image_blob.make_public()
    url = image_blob.public_url  # image_blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    stored.image = url
    db.commit()
    return stored


def upload_cover(profile_id: str, db: Session, file: UploadFile = File(...)):
    """

    :param db:
    :param file:
    :param profile_id:
    :return:
    """
    stored = db.query(models.Profile).filter(models.Profile.id == profile_id).first()

    image_name = str(uuid.uuid4().hex) + '.png'
    image_blob = bucket.blob('profiles/covers/' + image_name)
    image_blob.upload_from_string(
        file.file.read(),
        content_type='image/png'
    )
    image_blob.make_public()
    url = image_blob.public_url  # image_blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    stored.cover = url

    db.commit()
    return stored


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

    stored.username = updated_profile.username
    stored.email = updated_profile.email
    stored.description = updated_profile.description
    stored.web = updated_profile.web
    stored.device_id = updated_profile.device_id
    stored.last_modification = datetime.datetime.now()

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
