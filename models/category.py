# src/models/product.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Category(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    # Relación virtual: Una categoría tiene muchos productos
    # back_populates conecta esta relación con la que definiremos en Product
    products = relationship("Product", back_populates="category")