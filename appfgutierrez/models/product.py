# src/models/product.py
from sqlalchemy import Column, Float, Integer, Numeric, String
from core.database import Base

class Product(Base):
    __tablename__ = "productos"

    # INVESTIGA Y COMPLETA:
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    stock = Column(Integer, default=0)
    precio = Column(Float, nullable=False)
    