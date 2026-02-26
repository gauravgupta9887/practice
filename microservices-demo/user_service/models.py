from sqlalchemy import Column, Integer, String, Numeric
from .shared.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    balance = Column(Numeric(10, 2), default=0)