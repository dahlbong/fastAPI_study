from sqlalchemy import Boolean, Column, DateTime, Integer, String

from core.db import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)

    username = Column(String(16), unique=True, index=True)
    password = Column(String(100))
    level = Column(String(100), nullable=False, default="guest")
    
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    registered_at = Column(DateTime, nullable=True, default=None)