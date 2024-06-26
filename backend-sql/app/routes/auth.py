from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from services.auth import signup, signin
from fastapi.responses import JSONResponse
from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup/",tags=["auth"] ,response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_username = crud.get_user_by_username(db, username=user.username)
    if db_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    try:
        created_user = signup(db=db, user=user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Account creation successful", "user": created_user})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Account creation failed", "error": str(e)})

@router.post("/signin/", tags=["auth"])
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    result = signin(db=db, user=user)

    if result["status"] == "failed":
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Signin failed", "detail": result["detail"]})
    response.set_cookie(key="auth", value=f"Bearer {result['token']}", httponly=True)
    return {"message": "Signin successful" , "token": result["token"]}