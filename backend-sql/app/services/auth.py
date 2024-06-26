import re
from fastapi import HTTPException
from ..db import crud, schemas
from ..extra.security import get_password_hash, verify_password, create_access_token
from sqlalchemy.orm import Session
from ..extra.RedisStorage import RedisStorage
from fastapi import Depends
from redis import Redis
from ..extra import config

config = config.get_config()
redis_storage = RedisStorage()
def signup(db: Session, user: schemas.UserCreate):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if not re.match(r"^[a-zA-Z0-9]+$", user.username):
        raise HTTPException(status_code=400, detail="Invalid username")

    created_user = crud.create_user(db=db, user=user)
    return created_user.to_dict()  # Convert the User object into a dictionary
res_object = RedisStorage()
def signin(db: Session, user: schemas.UserLogin):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        return {"status": "failed", "detail": "Invalid email or password"}

    payload = {"uid": db_user.id, "username": db_user.username, "display_name": db_user.display_name}
    token = create_access_token(payload, redis_storage)
    return {"status": "success", "token": token}