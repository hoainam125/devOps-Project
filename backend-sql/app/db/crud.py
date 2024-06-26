from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import User
from .schemas import UserCreate, UserLogin
from .. extra.security import get_password_hash, verify_password
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)  # Example function to hash password
    db_user = User(email=user.email, username=user.username, display_name=user.display_name, password=hashed_password)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None

def authenticate_user(db: Session, login_data: UserLogin):
    user = db.query(User).filter(User.email == login_data.email).first()
    if user and verify_password(login_data.password, user.password):  # Example function to verify password
        return user
    return None