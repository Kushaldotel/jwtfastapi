from sqlalchemy.orm import Session
from db.models import User
from .auth import get_password_hash, verify_password

def create_user(db: Session, user_data):
    user = User(
        name=user_data.name,
        email=user_data.email,
        location=user_data.location,
        about=user_data.about,
        password=get_password_hash(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user
