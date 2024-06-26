from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from services.auth import signup, signin, oAuth
from fastapi.responses import JSONResponse
from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/me/",tags=["user"] ,response_model=schemas.oAuthResponse)
def oAuth_user(token: schemas.Token, db: Session = Depends(get_db)):
    token = token.token
    result = oAuth(db, token)
    if(result["status"] == "failed"):
        raise HTTPException(status_code=400, detail="Invalid Token")
    return result
