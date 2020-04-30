# Uvicorn
import uvicorn

# Utils
from typing import List

# Fast Api
from fastapi import FastAPI, HTTPException, Depends, UploadFile

# SQL Alchemy
from fastapi.params import File
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

    account = crud.create_profile(db=db, profile=profile)

    """consumer_url = 'http://localhost:8001/consumers'

    consumer_data = {
        'username': account.email,
        'custom_id': account.id
    }
    response = requests.post(url=consumer_url, data=consumer_data)

    basic_auth_url = 'http://localhost:8001/consumers/{0}/basic-auth'.format(account.email)

    basic_auth_data = {
        'username': account.email,
        'password': "password"
    }

    response = requests.post(url=basic_auth_url, data=basic_auth_data)

    api_key_url = 'http://localhost:8001/consumers/{0}/key-auth'.format(account.email)

    response = requests.post(url=api_key_url)"""

    return account


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
    if profiles is None:
        raise HTTPException(status_code=500, detail="Internal server error, could not find the specification")
    return profiles


@app.get("/profiles/basic/list/", response_model=List[schemas.BasicProfile], tags=['Profiles'])
def basic_list_data(profiles_id: List[str], db: Session = Depends(get_db)):
    """

    :param profiles_id:
    :param db:
    :return:
    """
    data = crud.get_profile_list_by_id(db=db, profiles_id=profiles_id)
    if data is None:
        raise HTTPException(status_code=500, detail="Internal server error, could not find the specification")
    return data


@app.get("/profiles/basic/{profile_id}", response_model=schemas.BasicProfile, tags=['Profiles'])
def basic_data(profile_id: str, db: Session = Depends(get_db)):
    """

    :param profile_id:
    :param db:
    :return:
    """
    data = crud.get_basic_data(db=db, profile_id=profile_id, )
    if data is None:
        raise HTTPException(status_code=500, detail="Internal server error, could not find the specification")
    return data


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
    if profiles is None:
        raise HTTPException(status_code=500, detail="Internal server error, could not find the specification")
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
    if profiles is None:
        raise HTTPException(status_code=500, detail="Internal server error, could not find the specification")
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


@app.patch("/profiles/user/picture/{profile_id}", response_model=schemas.Profile, tags=['Profiles'])
def update_picture(profile_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """

    :param file:
    :param profile_id:
    :param db:
    :return:
    """
    picture = crud.upload_image(db=db, profile_id=profile_id, file=file)
    if picture is None:
        raise HTTPException(status_code=500, detail="Error uploading the image")
    return picture


@app.patch("/profiles/", response_model=schemas.Profile, tags=['Profiles'])
def update_profile(profile: schemas.Profile, db: Session = Depends(get_db)):
    """
    Calls the crud function update_profile() and send the parameters it needs,
    if the db_profile var gets a None it raise an http exception if it's not None it returns
    the object.
    :param file:
    :param profile: profile data we wan't to update
    :param db: database connection
    :return:
    """
    db_profile = crud.update_profile(db, profile=profile)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.patch("/profiles/deactivate/{profile_id}", response_model=schemas.ProfileStatus, tags=['Profiles'])
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


@app.patch("/profiles/activate/{profile_id}", response_model=schemas.ProfileStatus, tags=['Profiles'])
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
