# src/models/product.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
