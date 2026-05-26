# src/models/product.py
from sqlalchemy import Column, Float, Integer, String
from core.database import Base

class Product(Base):
    __tablename__ = "productos"

    # INVESTIGA Y COMPLETA:
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    stock = Column(Integer, default=0)
    precio = Column(Float, nullable=False)
    
    # 1. La Llave Foránea Física en MySQL
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="CASCADE"), nullable=False)

    # 2. La Relación Virtual en Python (Para navegar entre objetos)
    category = relationship("Category", back_populates="products")