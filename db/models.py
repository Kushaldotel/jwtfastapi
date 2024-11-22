from sqlalchemy import Column, String, Integer
from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    location = Column(String, nullable=True)
    about = Column(String, nullable=True)
    password = Column(String, nullable=False)
