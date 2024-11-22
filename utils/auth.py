from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.models import User
from db.schemas import TokenData
from db.database import get_db

SECRET_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCYT/NTGCRhv4tpOUi9YYwD/hvI/sVNn8cgZi43pLJwRvqVowKT
QHsO/Io1B1Gvu/GGTrK5Ouq+WunTLGLgVwJkmuximblzjaLXHLS2TTkdCM4h0Hzo
2YnUZjWK/pmHW/SsZg96btsoVn2WRiM4b4yAeyz19oKInmj98YssgeUX6QIDAQAB
AoGARhDhWmRMuDqpIyqa76OkCWIn3fp1QRQzQhA/SpGVFFlShOuMD7kl4usBmQtY
5IKMxMAHL3aO7ipcTiyo/5KHIpMDeY7JuVwKztlxIkhmFm/nJRr+pgdxMUy4NWSG
rVLJtLwOl2x5+c4coo+YVOyt4jFTMQWB9Y7Sstj16vt5zgECQQDHKW6bmZII0DYU
W4If8K4i1QtUWvDzn/f+pExUDci7h7hi7vOl/7nOdA9a01AYT/fwUqPWpO3dUWH2
kmXSn1OZAkEAw8e8x3IcXdQiCFCLfWexC/eeZdG7he7QS+gLGZRSgE1eetyzhoKX
hv9dlLV1+C0oDWfNYVw8oOP3lsQp4weY0QJBAKvYUBvqclswbLk8DBdLMLXVZaUv
ouBTk0Qgt8t+6UkGXk7fJ1SARu6gre8MjfusZJ70b3HxdVyVsBV1VG5cE2ECQG50
z1Y7VDO/zl+gicJ78RCOaOiLNuBuh0h8J18MJqvKeuaYhBT8st7wTmzrIB6f43wE
t4QZlP80/ugpznQPQjECQDTSzUyhLtcZTrUyvo62xP0Vi2GH4iK+BP2a3c2DegQz
KEydFqL9ghgVDygfVX3NijXws1St2GfDkzkAl454dmA=
-----END RSA PRIVATE KEY-----"""  # Replace with your RSA private key if using RS256

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day for example

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Password hashing and verification
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# JWT token creation
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Extract the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        token_data = TokenData(email=email)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.email == token_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode JWT token
def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")