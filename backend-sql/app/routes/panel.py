from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..services.auth import signup, signin
from fastapi.responses import JSONResponse
from ..db import crud, models, schemas
from ..db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

