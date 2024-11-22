from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from db.database import engine, get_db
from db import models, schemas  # Ensure models are imported here
from utils import crud, auth
from utils.auth import create_access_token,create_refresh_token,decode_jwt_token


# Ensure metadata is created only once after importing models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/v1/register-user", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@app.post("/api/v1/auth/login", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate user by username and password
    user = crud.authenticate_user(db, form_data.username, form_data.password)

    # If user is not found or password is invalid
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate access token for the user
    access_token = auth.create_access_token({"sub": user.email})

    # Generate a refresh token (optional, can be used for token refreshing)
    refresh_token = auth.create_access_token({"sub": user.email, "scope": "refresh"})

    # Return the access and refresh tokens
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@app.get("/api/v1/me", response_model=schemas.UserResponse)
def get_profile(current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    return current_user


# /refresh-token endpoint (to refresh the access token)
@app.post("/api/v1/auth/refresh-token", response_model=schemas.Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    # Decode the refresh token
    payload = decode_jwt_token(refresh_token)

    # Optionally: Add checks like validating the "scope" of the refresh token, etc.
    # For now, we just check if the token is valid and not expired.

    # Generate a new access token using the data from the refresh token
    new_access_token = create_access_token({"sub": payload.get("sub")})
    new_refresh_token = create_refresh_token({"sub": payload.get("sub")})

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "Bearer"}