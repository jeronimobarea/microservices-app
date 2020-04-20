# Uvicorn
import time

import uvicorn

# Utils
from datetime import datetime
from typing import List

# Fast Api
from fastapi import FastAPI, HTTPException, Depends, Request, Response

# SQL Alchemy
from sqlalchemy.orm import Session

# Project files
from starlette.responses import RedirectResponse

from src import crud, models, schemas

# Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Database config
from src.database import SessionLocal, engine

"""
Creation of the models in the database.
"""
models.Base.metadata.create_all(bind=engine)

"""
FastApi connection.
debug=True for seeing the errors. 
"""
app = FastAPI(debug=True)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)


def get_db():
    """
    Basic connection with the database.
    :return:
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Routes
@app.get("/", tags=['Root'])
def read_root():
    """
    Root is a blank root that redirects to profiles
    :return:
    """
    return RedirectResponse('/profiles/')


@app.post("/profiles/", response_model=schemas.Profile, tags=['Profiles'])
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    """
    Calls to the crud function get_profile_by_email() and sends the parameters it needs,
    if the do_profile var gets a None it raise an http exception if it's not None it returns
    the object.
    :param profile: profile data
    :param db: database connection
    :return:
    """
    db_profile = crud.get_profile_by_email(db, email=profile.email)
    if db_profile:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_profile(db=db, profile=profile)


@app.get("/profiles/", response_model=schemas.Pagination, tags=['Profiles'])
def read_profiles(pagination: schemas.Pagination, db: Session = Depends(get_db)):
    """
    Calls the crud function get_profiles() and send the parameters it needs,
    if the profile var gets a None it raise an http exception if it's not None it returns
    the object.
    :param pagination: schema that contains the page number and the items per page
    :param db: database connection
    :return:
    """
    profiles = crud.get_profiles(db, page=pagination.page, per_page=pagination.per_page, )
    return profiles


@app.get("/profiles/active/", response_model=schemas.Pagination, tags=['Profiles'])
def read_active_profiles(pagination: schemas.Pagination, db: Session = Depends(get_db)):
    """
    Calls the crud function get_active_profiles() and send the parameters it needs,
    if the profile var gets a None it raise an http exception if it's not None it returns
    the object.
    :param pagination: schema that contains the page number and the items per page
    :param db: database connection
    :return:
    """
    profiles = crud.get_active_profiles(db, page=pagination.page, per_page=pagination.per_page, )
    return profiles


@app.get("/profiles/inactive/", response_model=schemas.Pagination, tags=['Profiles'])
def read_inactive_profiles(pagination: schemas.Pagination, db: Session = Depends(get_db)):
    """
    Calls the crud function get_inactive_profiles() and send the parameters it needs,
    if the profile var gets a None it raise an http exception if it's not None it returns
    the object.
    :param pagination: schema that contains the page number and the items per page
    :param db: database connection
    :return:
    """
    profiles = crud.get_inactive_profiles(db, page=pagination.page, per_page=pagination.per_page, )
    return profiles


@app.get("/profiles/{profile_id}", response_model=schemas.Profile, tags=['Profiles'])
def read_profile(profile_id: str, db: Session = Depends(get_db)):
    """
    Calls the crud function get_profile() and send the parameters it needs,
    if the db_profile var gets a None it raise an http exception if it's not None it returns
    the object.
    :param profile_id: id of the user we wan't
    :param db: database connection
    :return:
    """
    db_profile = crud.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.patch("/profiles/", response_model=schemas.Profile, tags=['Profiles'])
def update_profile(profile: schemas.Profile, db: Session = Depends(get_db)):
    """
    Calls the crud function update_profile() and send the parameters it needs,
    if the db_profile var gets a None it raise an http exception if it's not None it returns
    the object.
    :param profile: profile data we wan't to update
    :param db: database connection
    :return:
    """
    db_profile = crud.update_profile(db, profile=profile)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.patch("/profiles/deactivate/{profile_id}", response_model=schemas.ProfileDelete, tags=['Profiles'])
def deactivate_profile(profile_id: str, db: Session = Depends(get_db)):
    """
    Calls the crud function deactivate() and send the parameters it needs,
    if the db_profile var gets a None it raise an http exception if it's not None it returns
    the object.
    :param profile_id: id of the profile we wan't to deactivate
    :param db: database connection
    :return:
    """
    db_profile = crud.deactivate(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.patch("/profiles/activate/{profile_id}", response_model=schemas.ProfileDelete, tags=['Profiles'])
def activate_profile(profile_id: str, db: Session = Depends(get_db)):
    """
    Calls the crud function activate() and send the parameters it needs,
    if the db_profile var gets a None it raise an http exception if it's not None it returns
    the object.
    :param profile_id: id of the profile we wan't to deactivate
    :param db: database connection
    :return:
    """
    db_profile = crud.activate(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


if __name__ == '__main__':
    uvicorn.run(app=app, host='http://127.0.0.1', port='8100', log_level="info", )
    # uvicorn main:app --reload --port 8100
